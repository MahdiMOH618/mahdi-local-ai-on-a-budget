# Hardware and runtime eras

Current workstation: two Intel Arc Pro B60 24GB cards; Intel Core i7-7700K (4 cores/8 threads,2017);64GB DDR4-2400 (4×16GB); ASUS PRIME Z270-A; Ubuntu24.04.5 LTS. The B60s use the xe driver and SYCL/Level Zero. Each card has a32GiB ReBAR window; each CPU PEG link was observed at PCIe3.0 x8. No serials, disk identifiers, hostnames or network addresses are distributed.

The28–31 October studies are a separate hardware era: generally16GiB system RAM and one B60 plus a GTX1080Ti11GB for the second service/vision work. CUDA used the1080Ti; these are not dual-B60 CUDA measurements. Some older tests paged, and their wall times must retain that limitation.

Runtime records: Bionic1.1.9 build6 with Vulkan runtime2.65.1 / llama.cpp b11908; official SYCL b11908 FP32/FP16 and later c3df4b7 source build; CUDA b11908/a4699400e with CUDA12.8; Strata native SYCL0.1.56 at ffa80d73133ea5c548aefe57889a16e8085a938f (Terminal product/version labels differ); Bolt SYCL459ab1cdd3c566168c814b6f50cb1a7e6eb79914; LiLiCorr Vulkan7592b61d3b53ca5b39a25a03508fa1246b78c579. Paired LiLiCorr speed arms use the exact same Vulkan executable.

The short successful hardware check exercised32GiB RAM with16 patterns, simultaneous checked FP16 GEMM on both cards, and previously44GiB of VRAM. It does not certify every byte of64GB system RAM or48GB VRAM,24/7 stability, PSU margins or theoretical peak GPU throughput.
