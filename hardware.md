# Hardware and runtime eras

Current workstation: two Intel Arc Pro B60 24 GB cards; Intel Core i7-7700K (4 cores/8 threads, 2017); 64 GB DDR4-2400 (4×16 GB); ASUS PRIME Z270-A; Ubuntu 24.04.5 LTS. The B60s use the xe driver and SYCL/Level Zero. Each card has a 32 GiB ReBAR window; each CPU PEG link was observed at PCIe 3.0 x8. No serials, disk identifiers, hostnames or network addresses are distributed.

The 28–31 October studies are a separate hardware era: generally 16 GiB system RAM and one B60 plus a GTX 1080 Ti 11 GB for the second service/vision work. CUDA used the 1080 Ti; these are not dual-B60 CUDA measurements. Some older tests paged, and their wall times must retain that limitation.

Runtime records: Bionic 1.1.9 build 6 with Vulkan runtime 2.65.1 / llama.cpp b11908; official SYCL b11908 FP32/FP16 and later c3df4b7 source build; CUDA b11908/a4699400e with CUDA 12.8; Strata native SYCL 0.1.56 at ffa80d73133ea5c548aefe57889a16e8085a938f (Terminal product/version labels differ); Bolt SYCL 459ab1cdd3c566168c814b6f50cb1a7e6eb79914; LiLiCorr Vulkan 7592b61d3b53ca5b39a25a03508fa1246b78c579. Paired LiLiCorr speed arms use the exact same Vulkan executable.

The short successful hardware check exercised 32 GiB RAM with 16 patterns, simultaneous checked FP16 GEMM on both cards, and previously 44 GiB of VRAM. It does not certify every byte of 64 GB system RAM or 48 GB VRAM, 24/7 stability, PSU margins or theoretical peak GPU throughput.
