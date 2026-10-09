package atds.jf02;

import com.dukascopy.api.*;
import com.dukascopy.api.system.ClientFactory;
import com.dukascopy.api.system.IClient;
import com.dukascopy.api.system.ISystemListener;

import java.io.BufferedWriter;
import java.io.IOException;
import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.time.Instant;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.util.Collections;
import java.util.Locale;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;

public final class JF02HistoryRead {
    private static final String JNLP_URL = "http://platform.dukascopy.com/demo_3/jforex_3.jnlp";
    private static final String INSTRUMENT_TEXT = "USATECH.IDX/USD";
    private static final long FROM_MS = 1759327200000L;
    private static final long TO_MS = 1759330799999L;
    private static final DateTimeFormatter TS =
            DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'", Locale.ROOT)
                    .withZone(ZoneOffset.UTC);

    public static void main(String[] args) throws Exception {
        String user = System.getenv("JFOREX_USER");
        String password = System.getenv("JFOREX_PASSWORD");
        String outputText = System.getenv("JF02_OUTPUT");
        String runLabel = System.getenv("JF02_RUN_LABEL");

        if (user == null || user.isEmpty() || password == null || password.isEmpty()) {
            System.err.println("JF02_CREDENTIALS_MISSING");
            System.exit(10);
        }
        if (outputText == null || outputText.isEmpty()) {
            System.err.println("JF02_OUTPUT_MISSING");
            System.exit(11);
        }
        if (!"READ_A".equals(runLabel) && !"READ_B".equals(runLabel)) {
            System.err.println("JF02_RUN_LABEL_INVALID");
            System.exit(12);
        }

        Path output = Paths.get(outputText).toAbsolutePath();
        Files.createDirectories(output.getParent());

        final CountDownLatch done = new CountDownLatch(1);
        final Collector strategy = new Collector(output, done);
        final IClient client = ClientFactory.getDefaultInstance();

        client.setSystemListener(new ISystemListener() {
            @Override public void onStart(long processId) { }
            @Override public void onStop(long processId) { }
            @Override public void onConnect() { }
            @Override public void onDisconnect() { }
        });

        Package apiPackage = Instrument.class.getPackage();
        String apiVersion = apiPackage == null ? null : apiPackage.getImplementationVersion();
        System.out.println("JF02_SDK_DEPENDENCY=3.6.51");
        System.out.println("JF02_API_IMPLEMENTATION_VERSION=" + (apiVersion == null ? "UNAVAILABLE" : apiVersion));
        System.out.println("JF02_RUN_LABEL=" + runLabel);
        System.out.println("JF02_INSTRUMENT=" + INSTRUMENT_TEXT);
        System.out.println("JF02_FROM_MS=" + FROM_MS);
        System.out.println("JF02_TO_MS_INCLUSIVE=" + TO_MS);

        client.connect(JNLP_URL, user, password);
        long deadline = System.currentTimeMillis() + 30000L;
        while (!client.isConnected() && System.currentTimeMillis() < deadline) {
            Thread.sleep(250L);
        }
        if (!client.isConnected()) {
            System.err.println("JF02_CONNECT_FAILED");
            System.exit(20);
        }

        client.startStrategy(strategy);

        if (!done.await(180, TimeUnit.SECONDS)) {
            System.err.println("JF02_TIMEOUT");
            client.disconnect();
            System.exit(21);
        }

        client.disconnect();
        if (!strategy.success) {
            System.err.println("JF02_FAILED=" + strategy.failure);
            System.exit(22);
        }

        System.out.println("JF02_SUCCESS");
        System.out.println("JF02_TICK_COUNT=" + strategy.tickCount);
        System.out.println("JF02_FIRST_MS=" + strategy.firstMs);
        System.out.println("JF02_LAST_MS=" + strategy.lastMs);
    }

    private static final class Collector implements IStrategy {
        private final Path output;
        private final Path partial;
        private final CountDownLatch done;
        private final AtomicBoolean terminal = new AtomicBoolean(false);
        private volatile boolean success = false;
        private volatile String failure = "UNSET";
        private volatile long tickCount = 0;
        private volatile long firstMs = -1;
        private volatile long lastMs = -1;
        private BufferedWriter writer;
        private IContext context;

        Collector(Path output, CountDownLatch done) {
            this.output = output;
            this.partial = Paths.get(output.toString() + ".partial");
            this.done = done;
        }

        @Override
        public void onStart(IContext context) throws JFException {
            this.context = context;
            final Instrument instrument = Instrument.fromString(INSTRUMENT_TEXT);
            if (instrument == null || !INSTRUMENT_TEXT.equals(instrument.toString())) {
                fail("BLOCKED_JF02_WRONG_INSTRUMENT");
                return;
            }

            context.setSubscribedInstruments(Collections.singleton(instrument), true);

            try {
                Files.deleteIfExists(partial);
                writer = Files.newBufferedWriter(
                        partial,
                        StandardCharsets.UTF_8,
                        StandardOpenOption.CREATE_NEW,
                        StandardOpenOption.WRITE
                );
                writer.write("timestamp,askPrice,bidPrice,askVolume,bidVolume\n");
            } catch (IOException e) {
                fail("BLOCKED_JF02_OUTPUT_OPEN");
                return;
            }

            try {
                java.util.List<ITick> ticks = context.getHistory().getTicks(
                        instrument,
                        FROM_MS,
                        TO_MS
                );

                if (ticks == null) {
                    fail("BLOCKED_JF02_HISTORY_LOAD_NULL");
                    return;
                }
                if (ticks.isEmpty()) {
                    fail("BLOCKED_JF02_EMPTY_RESPONSE");
                    return;
                }

                for (ITick tick : ticks) {
                    if (terminal.get()) return;
                    acceptTick(
                            instrument,
                            tick.getTime(),
                            tick.getAsk(),
                            tick.getBid(),
                            tick.getAskVolume(),
                            tick.getBidVolume()
                    );
                }
                finishSuccess();
            } catch (JFException e) {
                fail(classifyHistoryFailure(e));
            } catch (IOException e) {
                fail("BLOCKED_JF02_OUTPUT_WRITE");
            } catch (RuntimeException e) {
                fail("BLOCKED_JF02_HISTORY_RUNTIME_FAILURE");
            }
        }

        private static String classifyHistoryFailure(Throwable error) {
            Throwable cursor = error;
            while (cursor != null) {
                if (cursor instanceof java.net.SocketTimeoutException) {
                    return "BLOCKED_JF02_HISTORY_NETWORK_TIMEOUT";
                }
                String message = cursor.getMessage();
                if (message != null && message.toLowerCase(Locale.ROOT).contains("timed out")) {
                    return "BLOCKED_JF02_HISTORY_NETWORK_TIMEOUT";
                }
                cursor = cursor.getCause();
            }
            return "BLOCKED_JF02_HISTORY_LOAD_FAILURE";
        }

        private synchronized void acceptTick(Instrument instrument, long time, double ask, double bid,
                                             double askVol, double bidVol) throws IOException {
            if (!INSTRUMENT_TEXT.equals(instrument.toString())) throw new IllegalStateException("WRONG_INSTRUMENT");
            if (time < FROM_MS || time > TO_MS) throw new IllegalStateException("INTERVAL_LEAK");
            if (lastMs >= 0 && time < lastMs) throw new IllegalStateException("SOURCE_ORDERING");
            if (!Double.isFinite(ask) || !Double.isFinite(bid) ||
                    !Double.isFinite(askVol) || !Double.isFinite(bidVol)) {
                throw new IllegalStateException("NONFINITE");
            }
            if (ask <= 0.0 || bid <= 0.0 || ask < bid) throw new IllegalStateException("PRICE_INVARIANT");
            if (askVol < 0.0 || bidVol < 0.0) throw new IllegalStateException("NEGATIVE_VOLUME");

            if (tickCount == 0) firstMs = time;
            lastMs = time;
            tickCount++;

            writer.write(TS.format(Instant.ofEpochMilli(time)));
            writer.write(',');
            writer.write(BigDecimal.valueOf(ask).toPlainString());
            writer.write(',');
            writer.write(BigDecimal.valueOf(bid).toPlainString());
            writer.write(',');
            writer.write(BigDecimal.valueOf(askVol).toPlainString());
            writer.write(',');
            writer.write(BigDecimal.valueOf(bidVol).toPlainString());
            writer.write('\n');
        }

        private synchronized void finishSuccess() {
            if (!terminal.compareAndSet(false, true)) return;
            try {
                writer.flush();
                writer.close();
                Files.move(partial, output, StandardCopyOption.REPLACE_EXISTING);
                success = true;
                failure = "NONE";
            } catch (IOException e) {
                success = false;
                failure = "BLOCKED_JF02_OUTPUT_FINALIZE";
                try { Files.deleteIfExists(partial); } catch (IOException ignored) { }
            } finally {
                done.countDown();
                if (context != null) context.stop();
            }
        }

        private synchronized void fail(String reason) {
            if (!terminal.compareAndSet(false, true)) return;
            success = false;
            failure = reason;
            try {
                if (writer != null) writer.close();
                Files.deleteIfExists(partial);
            } catch (IOException ignored) { }
            done.countDown();
            if (context != null) {
                try { context.stop(); } catch (Exception ignored) { }
            }
        }

        @Override public void onTick(Instrument instrument, ITick tick) { }
        @Override public void onBar(Instrument instrument, Period period, IBar askBar, IBar bidBar) { }
        @Override public void onMessage(IMessage message) { }
        @Override public void onAccount(IAccount account) { }
        @Override public void onStop() { }
    }
}
