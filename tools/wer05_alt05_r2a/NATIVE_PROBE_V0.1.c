/* ATDS WER-05 ALT-05 R1: fixed-source bounded Win64 controlled Job probe.
 * Roles: --controller (starts independent observer before worker creation),
 *        --observer (independent of controller, owns duplicated limited handles).
 * No CRT, no file I/O, no networking, no ETW; only allowlisted stdout verdicts.
 * STATIC CANDIDATE: MUST BE QUALIFIED before any GitHub execution.
 */
typedef void* HANDLE;
typedef unsigned long DWORD;
typedef unsigned short WORD;
typedef unsigned char BYTE;
typedef int BOOL;
typedef unsigned long long QWORD;
typedef unsigned long long ULONG_PTR;
typedef unsigned long long SIZE_T;
typedef unsigned short WCHAR;
#define NULL ((void*)0)
#define API __declspec(dllimport)
#define WINAPI __stdcall
#define WAIT_OBJECT_0 0u
#define WAIT_TIMEOUT 258u
#define CREATE_SUSPENDED 0x00000004u
#define CREATE_NO_WINDOW 0x08000000u
#define EXTENDED_STARTUPINFO_PRESENT 0x00080000u
#define PROC_THREAD_ATTRIBUTE_HANDLE_LIST 0x00020002u
#define STARTF_USESTDHANDLES 0x00000100u
#define HANDLE_FLAG_INHERIT 0x00000001u
#define DUPLICATE_CLOSE_SOURCE 0x00000001u
#define PROCESS_QUERY_LIMITED_INFORMATION 0x00001000u
#define SYNCHRONIZE 0x00100000u
#define JOB_OBJECT_QUERY 0x0004u
#define JOB_OBJECT_TERMINATE 0x0008u
#define JOB_OBJECT_LIMIT_ACTIVE_PROCESS 0x00000008u
#define JOB_OBJECT_LIMIT_JOB_MEMORY 0x00000200u
#define JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE 0x00002000u
#define STD_INPUT_HANDLE ((DWORD)-10)
#define STD_OUTPUT_HANDLE ((DWORD)-11)

typedef struct { DWORD nLength; void* lpSecurityDescriptor; BOOL bInheritHandle; } SECURITY_ATTRIBUTES;
typedef struct { DWORD cb; WCHAR* lpReserved; WCHAR* lpDesktop; WCHAR* lpTitle; DWORD dwX; DWORD dwY; DWORD dwXSize; DWORD dwYSize; DWORD dwXCountChars; DWORD dwYCountChars; DWORD dwFillAttribute; DWORD dwFlags; WORD wShowWindow; WORD cbReserved2; BYTE* lpReserved2; HANDLE hStdInput; HANDLE hStdOutput; HANDLE hStdError; } STARTUPINFOW;
typedef struct { STARTUPINFOW StartupInfo; void* lpAttributeList; } STARTUPINFOEXW;
typedef struct { HANDLE hProcess; HANDLE hThread; DWORD dwProcessId; DWORD dwThreadId; } PROCESS_INFORMATION;
typedef struct { DWORD dwLowDateTime; DWORD dwHighDateTime; } FILETIME;
typedef struct { long long PerProcessUserTimeLimit; long long PerJobUserTimeLimit; DWORD LimitFlags; ULONG_PTR MinimumWorkingSetSize; ULONG_PTR MaximumWorkingSetSize; DWORD ActiveProcessLimit; ULONG_PTR Affinity; DWORD PriorityClass; DWORD SchedulingClass; } JOBOBJECT_BASIC_LIMIT_INFORMATION;
typedef struct { QWORD ReadOperationCount; QWORD WriteOperationCount; QWORD OtherOperationCount; QWORD ReadTransferCount; QWORD WriteTransferCount; QWORD OtherTransferCount; } IO_COUNTERS;
typedef struct { JOBOBJECT_BASIC_LIMIT_INFORMATION BasicLimitInformation; IO_COUNTERS IoInfo; SIZE_T ProcessMemoryLimit; SIZE_T JobMemoryLimit; SIZE_T PeakProcessMemoryUsed; SIZE_T PeakJobMemoryUsed; } JOBOBJECT_EXTENDED_LIMIT_INFORMATION;
typedef struct { long long TotalUserTime; long long TotalKernelTime; long long ThisPeriodTotalUserTime; long long ThisPeriodTotalKernelTime; DWORD TotalPageFaultCount; DWORD TotalProcesses; DWORD ActiveProcesses; DWORD TotalTerminatedProcesses; } JOBOBJECT_BASIC_ACCOUNTING_INFORMATION;
typedef struct { DWORD NumberOfAssignedProcesses; DWORD NumberOfProcessIdsInList; ULONG_PTR ProcessIdList[4]; } JOBOBJECT_BASIC_PROCESS_ID_LIST4;

typedef struct { DWORD magic; DWORD phase; QWORD worker_handle; QWORD job_handle; QWORD creation_time; DWORD status; DWORD total; DWORD active; DWORD reserved; } PACKET;
#define MAGIC 0xA7050001u
#define PHASE_READY 1u
#define PHASE_LINK 2u
#define PHASE_BOUND 3u
#define PHASE_FINAL 4u
#define PHASE_FAIL 5u

API BOOL WINAPI CreateProcessW(const WCHAR*, WCHAR*, SECURITY_ATTRIBUTES*, SECURITY_ATTRIBUTES*, BOOL, DWORD, void*, const WCHAR*, STARTUPINFOW*, PROCESS_INFORMATION*);
API DWORD WINAPI GetModuleFileNameW(HANDLE, WCHAR*, DWORD);
API HANDLE WINAPI CreateJobObjectW(SECURITY_ATTRIBUTES*, const WCHAR*);
API BOOL WINAPI SetInformationJobObject(HANDLE, DWORD, const void*, DWORD);
API BOOL WINAPI AssignProcessToJobObject(HANDLE, HANDLE);
API BOOL WINAPI IsProcessInJob(HANDLE, HANDLE, BOOL*);
API BOOL WINAPI QueryInformationJobObject(HANDLE, DWORD, void*, DWORD, DWORD*);
API BOOL WINAPI GetProcessTimes(HANDLE, FILETIME*, FILETIME*, FILETIME*, FILETIME*);
API DWORD WINAPI GetProcessId(HANDLE);
API DWORD WINAPI WaitForSingleObject(HANDLE, DWORD);
API BOOL WINAPI GetExitCodeProcess(HANDLE, DWORD*);
API BOOL WINAPI TerminateProcess(HANDLE, DWORD);
API BOOL WINAPI TerminateJobObject(HANDLE, DWORD);
API HANDLE WINAPI GetCurrentProcess(void);
API BOOL WINAPI DuplicateHandle(HANDLE, HANDLE, HANDLE, HANDLE*, DWORD, BOOL, DWORD);
API BOOL WINAPI CreatePipe(HANDLE*, HANDLE*, SECURITY_ATTRIBUTES*, DWORD);
API BOOL WINAPI SetHandleInformation(HANDLE, DWORD, DWORD);
API HANDLE WINAPI GetStdHandle(DWORD);
API BOOL WINAPI ReadFile(HANDLE, void*, DWORD, DWORD*, void*);
API BOOL WINAPI WriteFile(HANDLE, const void*, DWORD, DWORD*, void*);
API BOOL WINAPI PeekNamedPipe(HANDLE, void*, DWORD, DWORD*, DWORD*, DWORD*);
API QWORD WINAPI GetTickCount64(void);
API void WINAPI Sleep(DWORD);
API DWORD WINAPI ResumeThread(HANDLE);
API BOOL WINAPI CloseHandle(HANDLE);
API BOOL WINAPI InitializeProcThreadAttributeList(void*, DWORD, DWORD, SIZE_T*);
API BOOL WINAPI UpdateProcThreadAttribute(void*, DWORD, ULONG_PTR, void*, SIZE_T, void*, SIZE_T*);
API void WINAPI DeleteProcThreadAttributeList(void*);
API HANDLE WINAPI GetProcessHeap(void);
API void* WINAPI HeapAlloc(HANDLE, DWORD, SIZE_T);
API BOOL WINAPI HeapFree(HANDLE, DWORD, void*);

static WCHAR exe_path[1024], observer_cmd[1024], worker_path[1024];
__attribute__((optnone)) void* memset(void* dst, int value, SIZE_T count) {
    BYTE* p=(BYTE*)dst;SIZE_T i;
    for(i=0;i<count;i++) p[i]=(BYTE)value;
    return dst;
}
static void close_if(HANDLE h) { if (h && h != (HANDLE)(-1)) (void)CloseHandle(h); }
static int send_packet(HANDLE h, const PACKET* p) { DWORD n=0; return WriteFile(h,p,(DWORD)sizeof(*p),&n,NULL) && n==(DWORD)sizeof(*p); }
static int recv_packet(HANDLE h, PACKET* p, DWORD max_ms) {
    DWORD a=0,n=0; QWORD end=GetTickCount64()+max_ms;
    while (GetTickCount64()<=end) {
        if (!PeekNamedPipe(h,NULL,0,NULL,&a,NULL)) return 0;
        if (a>=sizeof(*p)) return ReadFile(h,p,(DWORD)sizeof(*p),&n,NULL) && n==(DWORD)sizeof(*p) && p->magic==MAGIC;
        Sleep(10);
    }
    return 0;
}
static QWORD ctime_of(HANDLE p) {
    FILETIME c,e,k,u;
    if (!GetProcessTimes(p,&c,&e,&k,&u)) return 0;
    return ((QWORD)c.dwHighDateTime<<32) | c.dwLowDateTime;
}
static int snapshot(HANDLE job, DWORD* total, DWORD* active, DWORD* assigned, DWORD* listed, ULONG_PTR* pid) {
    JOBOBJECT_BASIC_ACCOUNTING_INFORMATION a={0};
    JOBOBJECT_BASIC_PROCESS_ID_LIST4 l={0};
    if (!QueryInformationJobObject(job,1,&a,sizeof(a),NULL)) return 0;
    if (!QueryInformationJobObject(job,3,&l,sizeof(l),NULL)) return 0;
    *total=a.TotalProcesses; *active=a.ActiveProcesses; *assigned=l.NumberOfAssignedProcesses; *listed=l.NumberOfProcessIdsInList;
    *pid=l.NumberOfProcessIdsInList==1?l.ProcessIdList[0]:0;
    return 1;
}
static void print_public(const char* s) {
    DWORD n=0,k=0; while(s[n]) n++;
    (void)WriteFile(GetStdHandle(STD_OUTPUT_HANDLE),s,n,&k,NULL);
}
static void copy_word(WCHAR* dst,const WCHAR* src) { while(*src) *dst++=*src++;*dst=0; }
static int make_path(const WCHAR* suffix, WCHAR* dst) {
    DWORD k=GetModuleFileNameW(NULL,dst,1000),i;
    if(k<4||k>=970) return 0;
    for(i=k;i>0;i--) if(dst[i-1]==L'\\') break;
    if(i==0) return 0;
    copy_word(dst+i,suffix); return 1;
}
static PACKET pkt(DWORD phase) { PACKET p={0};p.magic=MAGIC;p.phase=phase;return p; }

static int observer(void) {
    HANDLE input=GetStdHandle(STD_INPUT_HANDLE),output=GetStdHandle(STD_OUTPUT_HANDLE),job=NULL,worker=NULL;
    PACKET q=pkt(PHASE_READY),r={0}; BOOL member=0;DWORD t=0,a=0,na=0,nl=0,code=0;ULONG_PTR pid=0;
    if (!send_packet(output,&q)) return 21;
    if (!recv_packet(input,&r,3000) || r.phase!=PHASE_LINK || !r.worker_handle || !r.job_handle || !r.creation_time) return 22;
    worker=(HANDLE)(ULONG_PTR)r.worker_handle;job=(HANDLE)(ULONG_PTR)r.job_handle;
    q=pkt(PHASE_FAIL);
    if (GetProcessId(worker)==0 || ctime_of(worker)!=r.creation_time) goto obs_fail;
    if (!IsProcessInJob(worker,job,&member) || !member) goto obs_fail;
    if (!snapshot(job,&t,&a,&na,&nl,&pid) || t!=1 || a!=1 || na!=1 || nl!=1 || pid!=(ULONG_PTR)GetProcessId(worker)) goto obs_fail;
    q=pkt(PHASE_BOUND);
    if (!send_packet(output,&q)) goto obs_fail;
    if (WaitForSingleObject(worker,8000)!=WAIT_OBJECT_0) goto obs_fail;
    if (!GetExitCodeProcess(worker,&code) || code!=0 || ctime_of(worker)!=r.creation_time) goto obs_fail;
    {
        DWORD i;int good=0;
        for(i=0;i<50;i++) {if(snapshot(job,&t,&a,&na,&nl,&pid)&&t==1&&a==0&&na==0&&nl==0){good=1;break;}Sleep(20);}
        if(!good) goto obs_fail;
    }
    q=pkt(PHASE_FINAL);q.status=1;q.total=t;q.active=a;
    (void)send_packet(output,&q);
    close_if(worker);close_if(job);return 0;
obs_fail:
    if(job) (void)TerminateJobObject(job,1);
    q=pkt(PHASE_FAIL);(void)send_packet(output,&q);
    close_if(worker);close_if(job);return 23;
}

static int controller(void) {
    SECURITY_ATTRIBUTES sa={0};HANDLE to_child_r=NULL,to_child_w=NULL,from_child_r=NULL,from_child_w=NULL,job=NULL;
    PROCESS_INFORMATION obs={0},worker={0};STARTUPINFOW si={0};STARTUPINFOEXW sex={0};void* attr=NULL;int attrInitialized=0;SIZE_T attrSize=0;HANDLE inheritOnly[2]={0};WCHAR* exe=exe_path;WCHAR* cmd=observer_cmd;WCHAR* wrk=worker_path;
    JOBOBJECT_EXTENDED_LIMIT_INFORMATION limits={0};PACKET q={0};
    BOOL assigned=0;HANDLE dupWorker=NULL,dupJob=NULL;QWORD birth=0;DWORD ec=1;
    sa.nLength=sizeof(sa);sa.bInheritHandle=1;
    if(!CreatePipe(&to_child_r,&to_child_w,&sa,0)) goto ctrl_fail;
    if(!CreatePipe(&from_child_r,&from_child_w,&sa,0)) goto ctrl_fail;
    if(!SetHandleInformation(to_child_w,HANDLE_FLAG_INHERIT,0)||!SetHandleInformation(from_child_r,HANDLE_FLAG_INHERIT,0)) goto ctrl_fail;
    if(!make_path(L"ATDS_ALT05_NATIVE_PROBE_V0.1.exe",exe)||!make_path(L"ATDS_ALT05_INERT_WORKER_V0.1.exe",wrk)) goto ctrl_fail;
    copy_word(cmd,exe);
    { DWORD i=0;while(cmd[i])++i;copy_word(cmd+i,L" --observer"); }
    /* Only these two explicit pipe handles may pass to the observer. */
    (void)InitializeProcThreadAttributeList(NULL,1,0,&attrSize);
    if(!attrSize) goto ctrl_fail;
    attr=HeapAlloc(GetProcessHeap(),0,attrSize);
    if(!attr||!InitializeProcThreadAttributeList(attr,1,0,&attrSize)) goto ctrl_fail;
    attrInitialized=1;
    inheritOnly[0]=to_child_r;inheritOnly[1]=from_child_w;
    if(!UpdateProcThreadAttribute(attr,0,PROC_THREAD_ATTRIBUTE_HANDLE_LIST,inheritOnly,sizeof(inheritOnly),NULL,NULL)) goto ctrl_fail;
    sex.StartupInfo.cb=sizeof(sex);sex.StartupInfo.dwFlags=STARTF_USESTDHANDLES;
    sex.StartupInfo.hStdInput=to_child_r;sex.StartupInfo.hStdOutput=from_child_w;sex.StartupInfo.hStdError=from_child_w;
    sex.lpAttributeList=attr;
    if(!CreateProcessW(exe,cmd,NULL,NULL,1,CREATE_NO_WINDOW|EXTENDED_STARTUPINFO_PRESENT,NULL,NULL,&sex.StartupInfo,&obs)) goto ctrl_fail;
    DeleteProcThreadAttributeList(attr);(void)HeapFree(GetProcessHeap(),0,attr);attr=NULL;attrInitialized=0;
    close_if(to_child_r);to_child_r=NULL;close_if(from_child_w);from_child_w=NULL;
    if(!recv_packet(from_child_r,&q,3000)||q.phase!=PHASE_READY) goto ctrl_fail;
    job=CreateJobObjectW(NULL,NULL);if(!job) goto ctrl_fail;
    limits.BasicLimitInformation.LimitFlags=JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE|JOB_OBJECT_LIMIT_ACTIVE_PROCESS|JOB_OBJECT_LIMIT_JOB_MEMORY;
    limits.BasicLimitInformation.ActiveProcessLimit=1;
    limits.JobMemoryLimit=32u*1024u*1024u;
    if(!SetInformationJobObject(job,9,&limits,sizeof(limits))) goto ctrl_fail;
    si.cb=sizeof(si);si.dwFlags=0;si.hStdInput=NULL;si.hStdOutput=NULL;si.hStdError=NULL;
    if(!CreateProcessW(wrk,NULL,NULL,NULL,0,CREATE_SUSPENDED|CREATE_NO_WINDOW,NULL,NULL,&si,&worker)) goto ctrl_fail;
    birth=ctime_of(worker.hProcess);if(!birth) goto ctrl_fail;
    assigned=AssignProcessToJobObject(job,worker.hProcess);if(!assigned) goto ctrl_fail;
    if(!DuplicateHandle(GetCurrentProcess(),worker.hProcess,obs.hProcess,&dupWorker,SYNCHRONIZE|PROCESS_QUERY_LIMITED_INFORMATION,0,0)) goto ctrl_fail;
    if(!DuplicateHandle(GetCurrentProcess(),job,obs.hProcess,&dupJob,JOB_OBJECT_QUERY|JOB_OBJECT_TERMINATE,0,0)) goto ctrl_fail;
    q=pkt(PHASE_LINK);q.worker_handle=(QWORD)(ULONG_PTR)dupWorker;q.job_handle=(QWORD)(ULONG_PTR)dupJob;q.creation_time=birth;
    if(!send_packet(to_child_w,&q)||!recv_packet(from_child_r,&q,3000)||q.phase!=PHASE_BOUND) goto ctrl_fail;
    if(ResumeThread(worker.hThread)!=1) goto ctrl_fail;
    if(!recv_packet(from_child_r,&q,11000)||q.phase!=PHASE_FINAL||q.status!=1||q.total!=1||q.active!=0) goto ctrl_fail;
    if(WaitForSingleObject(worker.hProcess,0)!=WAIT_OBJECT_0||ctime_of(worker.hProcess)!=birth) goto ctrl_fail;
    if(!GetExitCodeProcess(worker.hProcess,&ec)||ec!=0) goto ctrl_fail;
    if(WaitForSingleObject(obs.hProcess,1000)!=WAIT_OBJECT_0) goto ctrl_fail;
    if(!GetExitCodeProcess(obs.hProcess,&ec)||ec!=0) goto ctrl_fail;
    print_public("ALT05_TARGETED_HANDLE_PROBE=PASS\n");
    close_if(worker.hThread);close_if(worker.hProcess);close_if(job);close_if(obs.hThread);close_if(obs.hProcess);
    close_if(to_child_w);close_if(from_child_r);return 0;
ctrl_fail:
    if(attr) { if(attrInitialized) DeleteProcThreadAttributeList(attr);(void)HeapFree(GetProcessHeap(),0,attr); }
    /* Assignment may have failed: terminate the known suspended worker directly as well. */
    if(worker.hProcess) (void)TerminateProcess(worker.hProcess,1);
    if(job) (void)TerminateJobObject(job,1);
    if(obs.hProcess) (void)TerminateProcess(obs.hProcess,1);
    print_public("ALT05_TARGETED_HANDLE_PROBE=BLOCKED\n");
    close_if(worker.hThread);close_if(worker.hProcess);close_if(job);close_if(obs.hThread);close_if(obs.hProcess);
    close_if(to_child_r);close_if(to_child_w);close_if(from_child_r);close_if(from_child_w);return 1;
}
int mainCRTStartup(void) {
    /* Avoid C runtime; child is explicitly launched with its role in the command line. */
    /* We use GetCommandLineW to discriminate the authorized observer invocation. */
    extern WCHAR* WINAPI GetCommandLineW(void);
    const WCHAR* p=GetCommandLineW();DWORD i=0;
    while (p&&p[i]) {
        if(p[i]==L'-'&&p[i+1]==L'-'&&p[i+2]==L'o'&&p[i+3]==L'b'&&p[i+4]==L's'&&p[i+5]==L'e'&&p[i+6]==L'r'&&p[i+7]==L'v'&&p[i+8]==L'e'&&p[i+9]==L'r') return observer();
        ++i;
    }
    return controller();
}
