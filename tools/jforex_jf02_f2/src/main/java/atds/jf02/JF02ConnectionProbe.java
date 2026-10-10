package atds.jf02;

import com.dukascopy.api.Instrument;
import com.dukascopy.api.system.ClientFactory;
import com.dukascopy.api.system.IClient;
import com.dukascopy.api.system.ISystemListener;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.Instant;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicReference;

public final class JF02ConnectionProbe {
    private static final String JNLP_URL = "http://platform.dukascopy.com/demo_3/jforex_3.jnlp";
    private static final String F2_CACHE_PATH_TEXT = "C:\\Users\\Boulevart\\ATDS-TOOLS\\jf02-f2-cache-v0.1";
    private static final String BASELINE_CACHE_PATH_TEXT = "C:\\Users\\Boulevart\\AppData\\Local\\JForex\\.cache";
    private static final String D3_CACHE_PATH_TEXT = "C:\\Users\\Boulevart\\ATDS-TOOLS\\jf02-d3-cache-v0.1";

    private static final long OBSERVATION_WINDOW_MS = 120000L;
    private static final long SAMPLE_INTERVAL_MS = 1000L;
    private static final long PRIMARY_THRESHOLD_MS = 30000L;
    private static final long DISCONNECT_OBSERVATION_MS = 10000L;

    private JF02ConnectionProbe() { }

    public static void main(String[] args) throws Exception {
        final String user = System.getenv("JFOREX_USER");
        final String secret = System.getenv("JFOREX_PASSWORD");

        if (user == null || user.trim().isEmpty() || secret == null || secret.isEmpty()) {
            System.err.println("F2_CREDENTIALS_MISSING");
            System.exit(10);
        }

        final Path f2Cache = Paths.get(F2_CACHE_PATH_TEXT).toAbsolutePath().normalize();
        final Path baselineCache = Paths.get(BASELINE_CACHE_PATH_TEXT).toAbsolutePath().normalize();
        final Path d3Cache = Paths.get(D3_CACHE_PATH_TEXT).toAbsolutePath().normalize();

        if (f2Cache.equals(baselineCache) || f2Cache.equals(d3Cache)) {
            System.err.println("BLOCKED_F2_PROTECTED_CACHE_SELECTED");
            System.exit(11);
        }
        if (Files.exists(f2Cache)) {
            System.err.println("BLOCKED_F2_CACHE_NOT_FRESH");
            System.exit(12);
        }

        final AtomicBoolean onConnectObserved = new AtomicBoolean(false);
        final AtomicBoolean onDisconnectObserved = new AtomicBoolean(false);
        final AtomicReference<String> onConnectUtc = new AtomicReference<String>(null);
        final AtomicReference<String> onDisconnectUtc = new AtomicReference<String>(null);

        final IClient client = ClientFactory.getDefaultInstance();
        client.setCacheDirectory(f2Cache.toFile());
        client.setSystemListener(new ISystemListener() {
            @Override
            public void onStart(long processId) { }

            @Override
            public void onStop(long processId) { }

            @Override
            public void onConnect() {
                if (onConnectObserved.compareAndSet(false, true)) {
                    String ts = Instant.now().toString();
                    onConnectUtc.set(ts);
                    System.out.println("F2_ONCONNECT_UTC=" + ts);
                }
            }

            @Override
            public void onDisconnect() {
                if (onDisconnectObserved.compareAndSet(false, true)) {
                    String ts = Instant.now().toString();
                    onDisconnectUtc.set(ts);
                    System.out.println("F2_ONDISCONNECT_UTC=" + ts);
                }
            }
        });

        Package apiPackage = Instrument.class.getPackage();
        String apiVersion = apiPackage == null ? null : apiPackage.getImplementationVersion();

        System.out.println("F2_SDK_DEPENDENCY=3.6.51");
        System.out.println("F2_API_IMPLEMENTATION_VERSION=" + (apiVersion == null ? "UNAVAILABLE" : apiVersion));
        System.out.println("F2_ACCOUNT_MODE=DEMO");
        System.out.println("F2_CACHE_PATH=" + f2Cache);
        System.out.println("F2_OBSERVATION_WINDOW_MS=" + OBSERVATION_WINDOW_MS);
        System.out.println("F2_SAMPLE_INTERVAL_MS=" + SAMPLE_INTERVAL_MS);
        System.out.println("F2_PRIMARY_THRESHOLD_MS=" + PRIMARY_THRESHOLD_MS);

        final String connectStartUtc = Instant.now().toString();
        final long connectStartNs = System.nanoTime();
        System.out.println("F2_CONNECT_CALL_START_UTC=" + connectStartUtc);
        System.out.println("F2_CONNECT_EXCEPTION_THROWN=false");

        try {
            client.connect(JNLP_URL, user, secret);
        } catch (Exception error) {
            long connectDurationMs = (System.nanoTime() - connectStartNs) / 1_000_000L;
            String exceptionClass = error.getClass().getName();
            String category = classifyConnectException(error);

            System.out.println("F2_CONNECT_CALL_DURATION_MS=" + connectDurationMs);
            System.out.println("F2_CONNECT_EXCEPTION_THROWN=true");
            System.out.println("F2_CONNECT_EXCEPTION_CLASS=" + exceptionClass);
            System.out.println("F2_CONNECT_EXCEPTION_CATEGORY=" + category);
            System.out.println("F2_RESULT=" + resultForException(category));
            System.exit(20);
            return;
        }

        final String connectReturnUtc = Instant.now().toString();
        final long connectDurationMs = (System.nanoTime() - connectStartNs) / 1_000_000L;
        System.out.println("F2_CONNECT_CALL_RETURN_UTC=" + connectReturnUtc);
        System.out.println("F2_CONNECT_CALL_DURATION_MS=" + connectDurationMs);

        final long observationStartNs = System.nanoTime();
        long firstConnectedElapsedMs = -1L;
        boolean everConnected = false;

        while (true) {
            long elapsedMs = (System.nanoTime() - observationStartNs) / 1_000_000L;
            boolean connected = client.isConnected();
            System.out.println("F2_ISCONNECTED_SAMPLE=" + elapsedMs + "," + connected);

            if (connected) {
                everConnected = true;
                firstConnectedElapsedMs = elapsedMs;
                break;
            }

            if (elapsedMs >= OBSERVATION_WINDOW_MS) {
                break;
            }

            long remainingMs = OBSERVATION_WINDOW_MS - elapsedMs;
            Thread.sleep(Math.min(SAMPLE_INTERVAL_MS, remainingMs));
        }

        String result;
        if (everConnected) {
            if (firstConnectedElapsedMs <= PRIMARY_THRESHOLD_MS) {
                result = "CONNECTED_WITHIN_ORIGINAL_BOUND";
            } else {
                result = "CONNECTED_ONLY_AFTER_ORIGINAL_BOUND";
            }
        } else if (onDisconnectObserved.get()) {
            result = "DISCONNECTED_BEFORE_FULL_INITIALIZATION";
        } else {
            result = "NOT_FULLY_CONNECTED_WITHIN_EXTENDED_BOUND";
        }

        System.out.println("F2_ONCONNECT_OBSERVED=" + onConnectObserved.get());
        System.out.println("F2_ONCONNECT_UTC_FINAL=" + valueOrNull(onConnectUtc.get()));
        System.out.println("F2_ONDISCONNECT_OBSERVED_BEFORE_INTENTIONAL=" + onDisconnectObserved.get());
        System.out.println("F2_ONDISCONNECT_UTC_BEFORE_INTENTIONAL=" + valueOrNull(onDisconnectUtc.get()));
        System.out.println("F2_FIRST_CONNECTED_ELAPSED_MS=" + firstConnectedElapsedMs);
        System.out.println("F2_RESULT=" + result);

        client.disconnect();

        long disconnectWaitStartNs = System.nanoTime();
        while (!onDisconnectObserved.get()) {
            long elapsedMs = (System.nanoTime() - disconnectWaitStartNs) / 1_000_000L;
            if (elapsedMs >= DISCONNECT_OBSERVATION_MS) {
                break;
            }
            Thread.sleep(100L);
        }

        System.out.println("F2_ONDISCONNECT_OBSERVED=" + onDisconnectObserved.get());
        System.out.println("F2_ONDISCONNECT_UTC_FINAL=" + valueOrNull(onDisconnectUtc.get()));
        System.out.println("F2_DONE=true");
    }

    private static String classifyConnectException(Throwable error) {
        String simple = error.getClass().getSimpleName();
        if ("JFAuthenticationException".equals(simple)) {
            return "AUTHENTICATION";
        }
        if ("JFVersionException".equals(simple)) {
            return "VERSION";
        }
        return "OTHER";
    }

    private static String resultForException(String category) {
        if ("AUTHENTICATION".equals(category)) {
            return "EXPLICIT_AUTHENTICATION_REJECTION";
        }
        if ("VERSION".equals(category)) {
            return "EXPLICIT_VERSION_REJECTION";
        }
        return "EXPLICIT_CONNECT_EXCEPTION";
    }

    private static String valueOrNull(String value) {
        return value == null ? "null" : value;
    }
}
