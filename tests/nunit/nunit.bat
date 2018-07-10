@echo off
csc /target:library /out:AcceptanceTests.dll /reference:nunit.framework.dll AcceptanceTests.cs
IF %ERRORLEVEL% == 0 nunit3-console AcceptanceTests.dll --workers=2 --process=Multiple --agents=50