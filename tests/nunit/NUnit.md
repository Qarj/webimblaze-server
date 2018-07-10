# NUnit integration

## Installation

### NUnit Framework
- Download NUnit framework: https://github.com/nunit/nunit/releases/tag/v3.10.1
- Place in folder `C:\cs` (should not matter)
- `cd C:\git\webinject-server\tests\nunit`
- `copy C:\cs\NUnit.Framework-3.10.1\bin\net40\nunit.framework.dll`
- Add csc to system path `C:\Windows\Microsoft.NET\Framework64\v4.0.30319`
- `csc /target:library /out:AcceptanceTests.dll /reference:nunit.framework.dll AcceptanceTests.cs`

### Install NUnit Console
- Download msi from https://github.com/nunit/nunit-console/releases
- Add to System path `C:\Program Files (x86)\NUnit.org\nunit-console`
- Run as `nunit3-console TestPrime.dll`

## Architecture

https://github.com/nunit/docs/wiki/TestContext


