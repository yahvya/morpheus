Package: openblas:x64-windows -> 0.3.24

**Host Environment**

- Host: x64-windows
- Compiler: MSVC 19.29.30152.0
-    vcpkg-tool version: 2023-09-15-ac02a9f660977426b8ec6392919fbb1d51b10998
    vcpkg-scripts version: a429a35bb 2023-11-07 (3 weeks ago)

**To Reproduce**

`vcpkg install `
**Failure logs**

```
-- Downloading https://github.com/xianyi/OpenBLAS/archive/v0.3.24.tar.gz -> xianyi-OpenBLAS-v0.3.24.tar.gz...
[DEBUG] To include the environment variables in debug output, pass --debug-env
[DEBUG] Trying to load bundleconfig from C:\Users\devel\.vcpkg-clion\vcpkg\vcpkg-bundle.json
[DEBUG] Failed to open: C:\Users\devel\.vcpkg-clion\vcpkg\vcpkg-bundle.json
[DEBUG] Bundle config: readonly=false, usegitregistry=false, embeddedsha=nullopt, deployment=Git, vsversion=nullopt
[DEBUG] Metrics enabled.
[DEBUG] Feature flag 'binarycaching' unset
[DEBUG] Feature flag 'compilertracking' unset
[DEBUG] Feature flag 'registries' unset
[DEBUG] Feature flag 'versions' unset
[DEBUG] Feature flag 'dependencygraph' unset
Downloading https://github.com/xianyi/OpenBLAS/archive/v0.3.24.tar.gz
warning: Download failed -- retrying after 1000ms
warning: Download failed -- retrying after 2000ms
warning: Download failed -- retrying after 4000ms
error: Failed to download from mirror set
error: https://github.com/xianyi/OpenBLAS/archive/v0.3.24.tar.gz: WinHttpReadData failed with exit code 12002
error: https://github.com/xianyi/OpenBLAS/archive/v0.3.24.tar.gz: WinHttpReadData failed with exit code 12030
error: https://github.com/xianyi/OpenBLAS/archive/v0.3.24.tar.gz: WinHttpReadData failed with exit code 12002
error: https://github.com/xianyi/OpenBLAS/archive/v0.3.24.tar.gz: WinHttpSendRequest failed with exit code 12007
[DEBUG] D:\a\_work\1\s\src\vcpkg\base\downloads.cpp(1051): 
[DEBUG] Time in subprocesses: 0us
[DEBUG] Time in parsing JSON: 6us
[DEBUG] Time in JSON reader: 0us
[DEBUG] Time in filesystem: 1710us
[DEBUG] Time in loading ports: 0us
[DEBUG] Exiting after 36 min (2168020389us)

CMake Error at scripts/cmake/vcpkg_download_distfile.cmake:32 (message):
      
      Failed to download file with error: 1
      If you are using a proxy, please check your proxy setting. Possible causes are:
      
      1. You are actually using an HTTP proxy, but setting HTTPS_PROXY variable
         to `https://address:port`. This is not correct, because `https://` prefix
         claims the proxy is an HTTPS proxy, while your proxy (v2ray, shadowsocksr
         , etc..) is an HTTP proxy. Try setting `http://address:port` to both
         HTTP_PROXY and HTTPS_PROXY instead.
      
      2. If you are using Windows, vcpkg will automatically use your Windows IE Proxy Settings
         set by your proxy software. See https://github.com/microsoft/vcpkg-tool/pull/77
         The value set by your proxy might be wrong, or have same `https://` prefix issue.
      
      3. Your proxy's remote server is out of service.
      
      If you've tried directly download the link, and believe this is not a temporary
      download server failure, please submit an issue at https://github.com/Microsoft/vcpkg/issues
      to report this upstream download server failure.
      

Call Stack (most recent call first):
  scripts/cmake/vcpkg_download_distfile.cmake:270 (z_vcpkg_download_distfile_show_proxy_and_fail)
  scripts/cmake/vcpkg_from_github.cmake:106 (vcpkg_download_distfile)
  buildtrees/versioning_/versions/openblas/c876665c0fa5b8d427ee9cadd4185a1a08d008da/portfile.cmake:1 (vcpkg_from_github)
  scripts/ports.cmake:168 (include)



```
**Additional context**

<details><summary>vcpkg.json</summary>

```
{
  "name": "test-opencv",
  "version-string": "1.0.0",
  "builtin-baseline": "01acfdfde3ed99280d3883a8fccd5fa4408f5214",
  "dependencies": [
    {
      "name": "opencv",
      "version>=": "4.8.0"
    },
    {
      "name": "dlib",
      "version>=": "19.24#2"
    }
  ]
}

```
</details>
