/* WER-05 ALT-05 v0.1 minimal worker — no CRT, no imports, no I/O. */
/* Returns 0 immediately; intended for a suspended process/job identity probe. */
int mainCRTStartup(void) { return 0; }
