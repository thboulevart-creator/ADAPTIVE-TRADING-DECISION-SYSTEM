"""F03 preregistered offline-only RED suite. No ClientFactory or network call."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools/jforex_fc01_jf02/src/main/java/atds/fc01jf02/FC01JF02HistoryRead.java"
TARGET = ROOT / "tools/jforex_fc01_jf02/target/classes"
RUNTIME = Path.home() / "ATDS-TOOLS/jforex-runtime-v0.1"
JAVA = RUNTIME / "jdk8/jdk8u504-b01/bin/java.exe"
JAVAC = RUNTIME / "jdk8/jdk8u504-b01/bin/javac.exe"
SDK = Path.home() / ".m2/repository/com/dukascopy/dds2/DDS2-jClient-JForex/3.6.51/DDS2-jClient-JForex-3.6.51.jar"
API = Path.home() / ".m2/repository/com/dukascopy/api/JForex-API/2.13.99/JForex-API-2.13.99.jar"

PROBE = r"""
import com.dukascopy.api.*;
import java.io.*;
import java.lang.reflect.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.CountDownLatch;

public final class F03Probe {
    static final long FROM = 1791446400000L;
    static final long TO = 1791449999999L;
    static LoadingDataListener callback;
    static LoadingProgressListener progress;
    static String invoked = "NONE";
    static String thrown = "NONE";

    static Object primitive(Class<?> cls) {
        if (cls == boolean.class) return false;
        if (cls == long.class) return 0L;
        if (cls == int.class) return 0;
        if (cls == double.class) return 0.0;
        if (cls == float.class) return 0f;
        return null;
    }

    static ITick tick(long time, double ask, double bid, double av, double bv) {
        return (ITick) Proxy.newProxyInstance(ITick.class.getClassLoader(),
                new Class<?>[]{ITick.class}, (p, m, a) -> {
                    switch(m.getName()) {
                        case "getTime": return time;
                        case "getAsk": return ask;
                        case "getBid": return bid;
                        case "getAskVolume": return av;
                        case "getBidVolume": return bv;
                    }
                    return primitive(m.getReturnType());
                });
    }

    static void feed(String scenario, Instrument instrument) {
        if ("null".equals(scenario) || "empty".equals(scenario)) {
            progress.loadingFinished(true, FROM, TO, TO);
            return;
        }
        long time = FROM;
        double ask = 25000.5, bid = 25000.0, av = 1.25, bv = 1.50;
        if ("invalid_price".equals(scenario)) ask = 24999.0;
        if ("invalid_volume".equals(scenario)) av = -1.0;
        if ("interval_leak".equals(scenario)) time = TO + 1;
        if ("source_order".equals(scenario)) time = FROM + 1;
        callback.newTick(instrument, time, ask, bid, av, bv);
        if ("source_order".equals(scenario)) {
            callback.newTick(instrument, time-1, ask, bid, av, bv);
        }
        progress.loadingFinished(true, FROM, TO, TO);
    }

    public static void main(String[] args) throws Exception {
        final String scenario = args[0];
        final Path output = Paths.get(args[1]).resolve("out.csv");
        if ("collision".equals(scenario)) {
            Files.write(output, "SENTINEL".getBytes(StandardCharsets.UTF_8));
        }
        Class<?> c = Class.forName("atds.fc01jf02.FC01JF02HistoryRead$Collector");
        Constructor<?> ctor = c.getDeclaredConstructor(Path.class, CountDownLatch.class);
        ctor.setAccessible(true);
        Object collector = ctor.newInstance(output, new CountDownLatch(1));
        IHistory history = (IHistory) Proxy.newProxyInstance(IHistory.class.getClassLoader(),
                new Class<?>[]{IHistory.class}, (p,m,a) -> {
                    String name = m.getName();
                    if ("getTicks".equals(name)) {
                        invoked = "getTicks";
                        if ("null".equals(scenario)) return null;
                        if ("empty".equals(scenario)) return Collections.emptyList();
                        if ("timeout".equals(scenario)) throw new JFException("Read timed out");
                        if ("timeout_during_load".equals(scenario)) {
                            Thread.sleep(80L);
                            throw new JFException("Read timed out");
                        }
                        if ("timeout_wrapped".equals(scenario)) throw new RuntimeException(
                                new java.net.SocketTimeoutException("Read timed out"));
                        if ("history_failure".equals(scenario)) throw new JFException("OTHER_HISTORY_FAILURE");
                        long tm=FROM;
                        double ask=25000.5, bid=25000.0, av=1.25, bv=1.50;
                        if ("invalid_price".equals(scenario)) ask=24999.0;
                        if ("invalid_volume".equals(scenario)) av=-1;
                        if ("interval_leak".equals(scenario)) tm=TO+1;
                        if ("source_order".equals(scenario)) tm=FROM+1;
                        List<ITick> values=new ArrayList<ITick>();
                        values.add(tick(tm,ask,bid,av,bv));
                        if ("source_order".equals(scenario)) values.add(tick(tm-1,ask,bid,av,bv));
                        return values;
                    }
                    if ("readTicks".equals(name)) {
                        invoked = "readTicks";
                        callback = (LoadingDataListener)a[3];
                        progress = (LoadingProgressListener)a[4];
                        if ("timeout".equals(scenario)) throw new JFException("Read timed out");
                        if ("timeout_during_load".equals(scenario)) {
                            Thread.sleep(80L);
                            throw new JFException("Read timed out");
                        }
                        if ("timeout_wrapped".equals(scenario)) throw new RuntimeException(
                                new java.net.SocketTimeoutException("Read timed out"));
                        if ("history_failure".equals(scenario)) throw new JFException("OTHER_HISTORY_FAILURE");
                        if (!"late_publish".equals(scenario) && !"output_write".equals(scenario)) {
                            feed(scenario,(Instrument)a[0]);
                        }
                        return null;
                    }
                    return primitive(m.getReturnType());
                });
        IContext context = (IContext) Proxy.newProxyInstance(IContext.class.getClassLoader(),
                new Class<?>[]{IContext.class}, (p,m,a) -> {
                    if ("getHistory".equals(m.getName())) return history;
                    return primitive(m.getReturnType());
                });
        Method start = c.getDeclaredMethod("onStart", IContext.class);
        start.setAccessible(true);
        try {
            start.invoke(collector, context);
        } catch(InvocationTargetException e) {
            Throwable cause=e.getCause();
            thrown=cause.getClass().getSimpleName()+":"+cause.getMessage();
        }
        if ("late_publish".equals(scenario) && callback!=null) {
            Method fail=c.getDeclaredMethod("fail",String.class);
            fail.setAccessible(true);
            fail.invoke(collector,"TEST_ABORT");
            feed("valid",Instrument.fromString("USATECH.IDX/USD"));
        }
        if ("output_write".equals(scenario) && callback!=null) {
            Field field=c.getDeclaredField("writer");
            field.setAccessible(true);
            field.set(collector, new BufferedWriter(new Writer() {
                public void write(char[] b,int s,int len) throws IOException {throw new IOException("SYNTHETIC_WRITE_FAIL");}
                public void flush() throws IOException {throw new IOException("SYNTHETIC_WRITE_FAIL");}
                public void close() {}
            }));
            feed("valid",Instrument.fromString("USATECH.IDX/USD"));
        }
        Field f=c.getDeclaredField("failure");f.setAccessible(true);
        Field s=c.getDeclaredField("success");s.setAccessible(true);
        System.out.println("METHOD="+invoked);
        System.out.println("FAIL="+f.get(collector));
        System.out.println("SUCCESS="+s.get(collector));
        System.out.println("THROWN="+thrown);
        System.out.println("FINAL="+Files.exists(output));
        System.out.println("PARTIAL="+Files.exists(Paths.get(output.toString()+".partial")));
        if(Files.exists(output)) {
            String raw=new String(Files.readAllBytes(output),StandardCharsets.UTF_8);
            System.out.println("ROWS="+raw.split("\\n").length);
            System.out.println("SENTINEL="+raw.equals("SENTINEL"));
            System.out.println("HAS_EXPECTED_PRICE="+raw.contains("25000.5,25000.0,1.25,1.5"));
        }
    }
}
"""


@pytest.fixture(scope="session")
def probe(tmp_path_factory):
    assert JAVA.is_file() and JAVAC.is_file() and SDK.is_file() and API.is_file() and TARGET.is_dir()
    directory = tmp_path_factory.mktemp("f03_offline_probe")
    source = directory / "F03Probe.java"
    source.write_text(PROBE, encoding="utf-8")
    classpath = os.pathsep.join([str(TARGET), str(SDK), str(API), str(directory)])
    result = subprocess.run([str(JAVAC), "-cp", classpath, str(source)],
                            capture_output=True, text=True, timeout=35)
    assert result.returncode == 0, result.stderr
    return directory, classpath


def run_case(probe, tmp_path, scenario):
    _, cp = probe
    result = subprocess.run([str(JAVA), "-Djava.awt.headless=true", "-cp", cp,
                             "F03Probe", scenario, str(tmp_path)],
                            capture_output=True, text=True, timeout=15)
    assert result.returncode == 0, (result.stdout, result.stderr)
    return dict(line.split("=", 1) for line in result.stdout.splitlines() if "=" in line)


@pytest.mark.parametrize("scenario,expected", [
    ("valid", "NONE"),
    ("null", "BLOCKED_FC01_JF02_HISTORY_LOAD_NULL"),
    ("empty", "BLOCKED_FC01_JF02_EMPTY_RESPONSE"),
    ("timeout", "BLOCKED_FC01_JF02_HISTORY_NETWORK_TIMEOUT"),
    ("timeout_wrapped", "BLOCKED_FC01_JF02_HISTORY_NETWORK_TIMEOUT"),
    ("timeout_during_load", "BLOCKED_FC01_JF02_HISTORY_NETWORK_TIMEOUT"),
    ("history_failure", "BLOCKED_FC01_JF02_HISTORY_LOAD_FAILURE"),
    ("invalid_price", "BLOCKED_FC01_JF02_TICK_VALIDATION:PRICE_INVARIANT"),
    ("invalid_volume", "BLOCKED_FC01_JF02_TICK_VALIDATION:NEGATIVE_VOLUME"),
    ("interval_leak", "BLOCKED_FC01_JF02_TICK_VALIDATION:INTERVAL_LEAK"),
    ("source_order", "BLOCKED_FC01_JF02_TICK_VALIDATION:SOURCE_ORDERING"),
    ("output_write", "BLOCKED_FC01_JF02_OUTPUT_WRITE"),
    ("collision", "BLOCKED_FC01_JF02_OUTPUT_FINALIZE"),
    ("late_publish", "TEST_ABORT"),
])
def test_synthetic_failure_separation(probe, tmp_path, scenario, expected):
    state = run_case(probe, tmp_path, scenario)
    assert state["FAIL"] == expected, state
    if scenario == "valid":
        assert state["SUCCESS"] == "true"
        assert state["FINAL"] == "true" and state["HAS_EXPECTED_PRICE"] == "true"
    elif scenario == "collision":
        assert state["SENTINEL"] == "true", state
    else:
        assert state["SUCCESS"] == "false"
        assert state["FINAL"] == "false", state
    assert state["PARTIAL"] == "false", state


def test_atomic_publication_without_silent_fallback():
    content=SOURCE.read_text(encoding="utf-8")
    assert "StandardCopyOption.ATOMIC_MOVE" in content
    assert "StandardCopyOption.REPLACE_EXISTING" not in content


def test_sync_history_primitive_and_fixed_binding():
    content=SOURCE.read_text(encoding="utf-8")
    assert ".getTicks(" in content
    assert ".readTicks(" not in content
    assert 'INSTRUMENT_TEXT = "USATECH.IDX/USD"' in content
    assert "1791446400000L" in content
    assert "1791449999999L" in content
    assert "1759327200000L" not in content


def test_canonical_serialization_and_order_preserved():
    content=SOURCE.read_text(encoding="utf-8")
    assert 'timestamp,askPrice,bidPrice,askVolume,bidVolume' in content
    assert all(("BigDecimal.valueOf("+k+").toPlainString()") in content
               for k in ["ask","bid","askVol","bidVol"])
    assert 'time < lastMs' in content
    assert '.sort(' not in content
    assert '.distinct(' not in content


def test_output_write_has_explicit_breaker():
    assert "BLOCKED_FC01_JF02_OUTPUT_WRITE" in SOURCE.read_text(encoding="utf-8")


def test_cancelled_execution_cannot_finalize_late():
    content=SOURCE.read_text(encoding="utf-8")
    assert "terminal.compareAndSet(false, true)" in content
    assert "terminal.get()" in content


def test_explicit_memory_and_blocking_contract():
    content=SOURCE.read_text(encoding="utf-8")
    assert "F03_MAX_HISTORY_TICKS" in content, "No predeclared bounded-resource mechanism"
    assert "F03_HISTORY_TIMEOUT" in content, "No explicit bounded synchronous loading mechanism"
