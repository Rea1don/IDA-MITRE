import idaapiimport idautilsimport idcimport ida_kernwinimport webbrowser  mitre_attack_mapping = {        "CreateProcessA": ("T1059", "Command-Line Interface"),    "CreateProcessW": ("T1059", "Command-Line Interface"),    "ShellExecuteA": ("T1059", "Command-Line Interface"),    "ShellExecuteW": ("T1059", "Command-Line Interface"),    "WinExec": ("T1059", "Command-Line Interface"),    "LoadLibraryA": ("T1106", "Execution through API"),    "LoadLibraryW": ("T1106", "Execution through API"),    "NtLoadDriver": ("T1215", "Kernel Modules and Extensions"),    "RtlCreateUserThread": ("T1106", "Execution through API"),       "VirtualAllocEx": ("T1055", "Process Injection"),    "WriteProcessMemory": ("T1055", "Process Injection"),    "CreateRemoteThread": ("T1055", "Process Injection"),    "NtCreateThreadEx": ("T1055", "Process Injection"),    "NtMapViewOfSection": ("T1055", "Process Injection"),    "ZwMapViewOfSection": ("T1055", "Process Injection"),    "QueueUserAPC": ("T1055", "Process Injection"),    "NtQueueApcThread": ("T1055", "Process Injection"),    "GetThreadContext": ("T1055", "Process Injection"),    "SetThreadContext": ("T1055", "Process Injection"),            "LsaRetrievePrivateData": ("T1003", "Credential Dumping: LSASS Memory"),    "LsaEnumerateLogonSessions": ("T1003", "Credential Dumping: LSASS Memory"),    "LsaQueryInformationPolicy": ("T1003", "Credential Dumping: LSASS Memory"),    "CryptUnprotectData": ("T1003.002", "Credential Dumping: Credentials in Files"),    "OpenProcessToken": ("T1134", "Access Token Manipulation"),    "DuplicateTokenEx": ("T1134", "Access Token Manipulation"),            "RegSetValueExA": ("T1112", "Modify Registry"),    "RegSetValueExW": ("T1112", "Modify Registry"),    "CreateServiceA": ("T1050", "New Service"),    "CreateServiceW": ("T1050", "New Service"),    "SetWindowsHookEx": ("T1179", "Hooking"),    "RegisterHotKey": ("T1546.002", "Event Triggered Execution"),    "CreateProcessAsUserA": ("T1055", "Process Injection"),    "CreateProcessAsUserW": ("T1055", "Process Injection"),        "CheckRemoteDebuggerPresent": ("T1622", "Debugger Evasion"),    "IsDebuggerPresent": ("T1622", "Debugger Evasion"),    "NtSetInformationThread": ("T1622", "Debugger Evasion"),    "ZwSetInformationThread": ("T1622", "Debugger Evasion"),    "NtQueryInformationProcess": ("T1018", "Discovery: Remote System Discovery"),    "NtClose": ("T1070.004", "Indicator Removal on Host"),      "InternetOpenA": ("T1071.001", "Application Layer Protocol: Web Protocols"),    "InternetOpenW": ("T1071.001", "Application Layer Protocol: Web Protocols"),    "InternetConnectA": ("T1071.001", "Application Layer Protocol: Web Protocols"),    "InternetConnectW": ("T1071.001", "Application Layer Protocol: Web Protocols"),    "HttpOpenRequestA": ("T1071.001", "Application Layer Protocol: Web Protocols"),    "HttpOpenRequestW": ("T1071.001", "Application Layer Protocol: Web Protocols"),    "WSASocketA": ("T1071.001", "Application Layer Protocol: Web Protocols"),    "WSASocketW": ("T1071.001", "Application Layer Protocol: Web Protocols"),    "connect": ("T1071.001", "Application Layer Protocol: Web Protocols"),        "FindFirstFileA": ("T1083", "File and Directory Discovery"),    "FindFirstFileW": ("T1083", "File and Directory Discovery"),    "FindNextFileA": ("T1083", "File and Directory Discovery"),    "FindNextFileW": ("T1083", "File and Directory Discovery"),    "GetFileAttributesA": ("T1083", "File and Directory Discovery"),    "GetFileAttributesW": ("T1083", "File and Directory Discovery"),      "NetScheduleJobAdd": ("T1031", "Scheduled Task"),    "WNetAddConnection2A": ("T1021.002", "SMB/Windows Admin Shares"),    "WNetAddConnection2W": ("T1021.002", "SMB/Windows Admin Shares"),        "RegOpenKeyExA": ("T1112", "Modify Registry"),    "RegOpenKeyExW": ("T1112", "Modify Registry"),    "RegDeleteKeyA": ("T1112", "Modify Registry"),    "RegDeleteKeyW": ("T1112", "Modify Registry"),    "RegQueryValueExA": ("T1112", "Modify Registry"),    "RegQueryValueExW": ("T1112", "Modify Registry"),            "AdjustTokenPrivileges": ("T1134", "Access Token Manipulation"),    "LookupPrivilegeValueA": ("T1134", "Access Token Manipulation"),    "LookupPrivilegeValueW": ("T1134", "Access Token Manipulation"),        "TerminateProcess": ("T1055", "Process Termination"),        "NtUnmapViewOfSection": ("T1070", "Indicator Removal on Host"),    "SuspendThread": ("T1071", "Application Layer Protocol: Custom Protocol"),          "SetWindowsHookExA": ("T1179", "Hooking"),    "SetWindowsHookExW": ("T1179", "Hooking"),    "GetAsyncKeyState": ("T1056.001", "Input Capture: Keylogging"),    "GetForegroundWindow": ("T1056", "Input Capture"),    "GetCursorPos": ("T1056", "Input Capture"),        "RtlAdjustPrivilege": ("T1134", "Access Token Manipulation"),    "NtRaiseHardError": ("T1069", "Permission Groups Discovery"),}class MitreAttckPlugin(idaapi.plugin_t):    flags = idaapi.PLUGIN_UNL    comment = "MITRE ATT&CK Plugin with UI"    help = ""    wanted_name = "MITRE ATT&CK"    wanted_hotkey = "Ctrl-Shift-M"    def init(self):        print("[*] MITRE ATT&CK Plugin initialized.")        return idaapi.PLUGIN_OK    def run(self, arg):        self.show_dialog()    def term(self):        print("[*] MITRE ATT&CK Plugin terminated.")    def show_dialog(self):        class MitreScanForm(ida_kernwin.Form):            def __init__(self):                self.results = []                super().__init__(                    r"""MITRE ATT&CK                   BY Muteb                    {FormChangeCb}                    <Start Scan:{iStartScan}><Results:{iShowResults}><LinkedIn:{iVisitProfile}>                    """,                     {                        'iStartScan': ida_kernwin.Form.ButtonInput(self.on_start_scan),                        'iShowResults': ida_kernwin.Form.ButtonInput(self.on_show_results),                        'iVisitProfile': ida_kernwin.Form.ButtonInput(self.on_visit_profile),                        'FormChangeCb': ida_kernwin.Form.FormChangeCb(self.OnFormChange),                    }                )            def OnFormChange(self, fid):                return 1            def on_start_scan(self, code=0):                print("[*] Starting scan for MITRE ATT&CK techniques...")                self.results = self.scan_for_mitre_techniques()                if not self.results:                    ida_kernwin.warning("No MITRE ATT&CK techniques found in this binary.")                else:                    ida_kernwin.info(f"Scan completed. Found {len(self.results)} MITRE ATT&CK techniques.")                print(f"[+] Scan completed. Found {len(self.results)} techniques.")            def on_show_results(self, code=0):                if not self.results:                    ida_kernwin.warning("Please run the scan first.")                else:                    print(f"[+] Displaying {len(self.results)} results in the chooser.")                    class ResultsChooser(ida_kernwin.Choose):                        def __init__(self, items):                            ida_kernwin.Choose.__init__(                                self,                                "MITRE ATT&CK Results",                                [["Address ↓", ida_kernwin.Choose.CHCOL_HEX | 10],                                 ["API ↓", ida_kernwin.Choose.CHCOL_PLAIN | 20],                                 ["MITRE ATT&CK ↓", ida_kernwin.Choose.CHCOL_PLAIN | 40]],                            )                            self.items = items                        def OnGetLine(self, n):                            return self.items[n]                        def OnGetSize(self):                            return len(self.items)                        def OnSelectLine(self, n):                                                  ea = int(self.items[n][0], 16)                              ida_kernwin.jumpto(ea)                                        results_list = [[hex(addr), func_name, mitre_technique] for addr, func_name, mitre_technique in self.results]                    chooser = ResultsChooser(results_list)                    chooser.Show()            def on_visit_profile(self, code=0):                                webbrowser.open("https://www.linkedin.com/in/muteb-bayomi-90ba96241?trk=public_post_feed-actor-name")            def scan_for_mitre_techniques(self):                results = []                               for function_ea in idautils.Functions():                    function_name = idc.get_func_name(function_ea)                    print(f"[*] Scanning function: {function_name}")                    for head in idautils.Heads(function_ea, idc.get_func_attr(function_ea, idc.FUNCATTR_END)):                        if idc.is_code(idc.get_full_flags(head)):                            mnemonic = idc.print_insn_mnem(head)                            operand = idc.print_operand(head, 0)                                                        print(f"Instruction at {hex(head)}: {mnemonic} {operand}")                            if operand in mitre_attack_mapping:                                attack_id, attack_desc = mitre_attack_mapping[operand]                                comment = f"{attack_desc} ({attack_id})"                                print(f"[+] Found MITRE technique at {hex(head)}: {comment}")                                idc.set_cmt(head, comment, 0)                                  results.append((head, function_name, f"{attack_id}: {attack_desc}"))                               print("[*] Checking import functions...")                for i in range(idaapi.get_import_module_qty()):                    import_name = idaapi.get_import_module_name(i)                    def imp_cb(ea, name, ordinal):                        if name and name in mitre_attack_mapping:                            attack_id, attack_desc = mitre_attack_mapping[name]                            print(f"[+] Found MITRE technique in imports: {name} ({attack_desc})")                            results.append((ea, name, f"{attack_id}: {attack_desc}"))                        return True                    idaapi.enum_import_names(i, imp_cb)                print(f"[+] Finished scanning. Total techniques found: {len(results)}")                return results        form = MitreScanForm()        form.Compile()        form.Execute()        form.Free()def PLUGIN_ENTRY():    return MitreAttckPlugin()