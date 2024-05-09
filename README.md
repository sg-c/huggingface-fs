# HuggingFace FS (HFFS)

## 什么是 HuggingFace FS (简称 "HFFS") ？

HuggingFace FS (简称 "HFFS") 目标成为一款“小而美”的工具，帮助中国大陆用户在使用 [HuggingFace](huggingface.co) 的时候，能够方便地下载、管理、分享来自 HF 的模型。

中国大陆用户通常需要配置代理服务才能访问 HuggingFace 主站。大陆地区和 HuggingFace 主站之间的网络带宽较低而且不稳定，可靠的镜像网站很少，模型文件又很大。因此，下载 HuggingFace 上模型文件的时间往往很长。HFFS 在 hf.co 的基础上增加了 P2P 的模型共享方式，让大陆地区用户能够以更快的速度获得所需要的模型。

HFFS 的典型使用场景有：
- 如果实验室或者开发部门的其他小伙伴已经下载了你需要的模型文件，HFFS 的 P2P 共享方式能让你从他们得到模型，模型的下载速度不再是个头疼的问题。当然，如果目标模型还没有被其他人下载过，HFFS 会自动从 hf.co 主站和镜像网站下载模型，然后你可以通过 HFFS 把模型分享给其他小伙伴。
- 有些小伙伴需要两台主机（Windows和Linux）完成模型的下载和使用：Windows 上的 VPN 很容易配置，所以它负责下载模型；Linux 的开发环境很方便，所以它负责模型的微调、推理等任务。通过 HFFS 的 P2P 共享功能，两台主机之间的模型下载和拷贝就不在再需要手动操作了。

下面是 HFFS 所提供的命令行文档。看看他们是如何帮助用户访问模型文件的吧。

## HFFS 的命令行

### HFFS 服务管理
```bash
hffs start
```
用户通过上面的命令开启本地 HFFS 服务。如果还未初始化，该命令则初始化 HFFS。
```bash
hffs stop [--destroy-cache]
```
用户通过上面的命令关闭本地 HFFS 服务。如果指定 --destory-cache 选项，则删除本地 MadFS 相关资源。

### Peer 管理
```bash
hffs peer add [HOST|IP|FILE]
```
用户通过上面的命令把 peer 节点配对：HFFS Daemon（节点A）和 HFFS Daemon（节点B）建立连接，此后可以互相访问。参数可以是目标节点的host或者ip地址（如果有多个值，用逗号隔开）；或者配置文件的路径（peer 配置文件可以同时指定多个 peer 地址。
```bash
hffs peer ls
```
用户通过上面的命令查看 peer 信息。
```bash
hffs peer rm [HOST|IP|FILE]
```
用户通过上面的命令删除 peer 节点。
### 模型管理
```bash
hffs model ls [repo-id]
```
扫描已经缓存的模型。该命令应该提供如下返回信息：repo-id, branch, revision, size on disk, num of files, local path, whether fully downoaded。
```bash
hffs model add repo-id [--branch BRANCH] [--revision REVISION]
```
下载指定的模型。
- 如果模型已经缓存，返回 hffs model ls repo-id 的返回信息。
- 如果模型还未缓存，从 peer 节点或者 hf.co 下载目标模型，显示下载进度条，结束后返回  hffs model ls repo-id 的返回信息。
```bash
hffs model rm repo-id [--branch BRANCH] [--revision REVISION]
```
删除缓存的模型数据。