# Oblique Orthographic Conduit

**Oblique Orthographic Conduit**（当前版本：v2.5 · Loader 1.0.1 · Windows x64） 是一款面向 Windows 的悬浮桌面工具，集成文本阅读与搜索、AI 对话和截图识别。

通过可调透明度、简洁的操作界面与平滑的窗口动画，让功能随手可用。

> Bringing seamless ease to your desktop，  
> Yielding control with a delicate grace.  
> Providing function without distraction,  
> Always lightweight, a silent interaction.  
> Simple design that hovers in view,  
> Softly transparent, yet always true.  
>
> Leaving no trace, it operates light,  
> Dynamically floating, just out of sight.  
> Balanced perfectly for those who demand.

<br>

## ✨ 功能

- **文本阅读与搜索**：载入本地文本，搜索关键词并切换匹配结果。
- **AI 对话**：使用自己的 API Key、接口地址与模型进行对话，支持数学公式显示。
- **截图识别**：截取屏幕并发送至配置的 AI 模型，同时保存截图到本地。
- **悬浮窗口**：调整透明度、字体、尺寸和位置，支持缩小为恢复按钮。
- **个性化设置**：通过设置界面或 `config.ini` 调整外观、快捷键和 AI 参数。
- **统一启动与更新**：由 `loader.exe` 管理 Alpha 启动、模块更新与 loader 自更新。

<br>

## 🚀 快速开始

1. 获取完整发布包 `OOC-v2.5-Windows-x64.zip`，解压到有写入权限的目录。
2. 联系作者获取授权，在 `config.ini` 中填写许可证和 AI 配置。
3. 双击运行 `loader.exe`。
4. 在 loader 中打开 **Alpha** 模块详情，点击 **Load** 启动。

发布版无需安装 Python。请保留完整目录结构：

```text
OOC/
├─ loader.exe       # 启动入口与更新管理
├─ config.ini       # 授权、AI、外观与快捷键配置
├─ _internal/       # 运行依赖
├─ app/             # Alpha 模块与运行状态
└─ docs/            # 使用说明及第三方许可证
```

`_internal` 和 `app` 需要与 `loader.exe` 一起保留。`loader-v3.zip` 是自动更新用的程序包，首次安装请使用完整发布包。

<br>

## ⚙️ 参数配置

编辑程序目录中的 `config.ini`，填写以下项目：

```ini
[License]
key = YOUR_LICENSE_KEY

[AI]
api_key = YOUR_API_KEY
base_url = YOUR_API_BASE_URL
model = YOUR_MODEL_NAME

[Screenshots]
directory = screenshots
```

- `License.key`：作者提供的许可证。Alpha 每次启动时需要联网验证授权与机器绑定。
- `AI.api_key`：你自己的 AI 服务密钥。
- `AI.base_url`：服务商提供的兼容 OpenAI Chat Completions 的 API 地址。
- `AI.model`：该服务商支持的模型名称；使用截图识别时需选择支持图片输入的模型。
- `Screenshots.directory`：截图保存目录。新版发布包默认使用程序目录下的 `screenshots`，保存时会尝试自动创建。

接口地址、密钥和模型应对应同一家服务商的配置。已有用户继续使用旧 `config.ini` 时，原来的截图路径与快捷键设置会保留。

启动 Alpha 后，点击 **A**，在输入框中输入 `/s` 并按回车，也可打开设置界面。

<br>

## 🎛️ 界面操作

以下字母和符号是**界面按钮的标签**。

| 按钮 | 功能 |
| --- | --- |
| `L` | 载入本地文本文档，建议使用 UTF-8 编码的 `.txt` 文件 |
| `U` | 卸载当前文档；载入文件后，`L` 会变为 `U` |
| `F` | 展开或收起搜索栏；输入关键词后按回车搜索 |
| `<` / `>` | 切换上一个／下一个搜索结果 |
| `A` | 切换 AI 对话与文本视图；在 AI 输入框中按回车发送 |
| `S` | 截取屏幕并发送给 AI，按钮位于 AI 输入栏中 |
| `–` | 将窗口缩为小型恢复按钮，点击恢复按钮重新展开 |

搜索按钮会在载入非空文本后显示。恢复按钮的尺寸与位置可在设置中调整，默认尺寸为 `2 × 2`，实际显示随系统缩放变化。

### AI 输入框中的本地命令

| 命令 | 功能 |
| --- | --- |
| `/s` | 打开设置界面 |
| `/exit` | 退出 Alpha |

输入命令后按回车执行。这两条命令在本地处理。

<br>

## ⌨️ 默认快捷键

| 快捷键 | 功能 |
| --- | --- |
| `Esc` | 将 Alpha 缩为恢复按钮 |
| `End` | 退出 Alpha |
| `Tab` | 截图并发送给 AI |
| `Home` | 显示或隐藏逐词显示窗口，有可用文本时生效 |
| `Page Up` / `Page Down` | 在逐词显示中切换上一个／下一个词 |
| `Ctrl + 鼠标滚轮` | 在主窗口中调整文字大小 |

除字体缩放操作外，上表列出的快捷键由程序注册为全局热键，可在设置界面或 `config.ini` 的 `[Hotkey]` 部分修改。若与其他软件冲突，请更换组合键。

<br>

## 🔄 自动更新

启动 loader 后，程序会在后台检查更新，并在窗口底部显示状态。Alpha 在加载前按检查周期检查更新，默认间隔为 24 小时。

当前更新源：[Google Drive 公开文件夹](https://drive.google.com/drive/folders/1TE7dOyaGBFJqtwm83zPLx3nsDmnEgmGk)。

- **loader 与依赖整体更新**，Alpha 模块独立更新。
- **Alpha 运行期间推迟安装 loader 更新**，空闲后自动安装并重启 loader。
- 下载完成后校验文件大小和 SHA-256；新 loader 启动失败时尝试恢复上一版本。
- 更新保留个人配置、许可证、主题和截图等用户数据。
- 更新检查失败时继续使用可用的本地版本；Alpha 的在线授权与 AI 服务仍需要网络连接。

关闭 loader 后，已启动的 Alpha 可以继续运行。重新打开 loader 可继续查看和管理该模块。

<br>

## ❓ FAQ 常见问题

**提示 `Update unavailable` 或 SSL 连接错误？**  
表示此次更新检查或下载未完成。请检查访问 Google Drive 的网络连接与代理设置，再重新启动 loader。已有可用本地版本会保留；仅凭这条提示无法确定具体的网络故障原因。

**Alpha 无法启动？**  
先检查 `[License] key` 是否正确、授权是否适用于当前机器，以及授权服务是否可以联网访问。

**AI 无响应或提示缺少 API Key？**  
检查 `[AI]` 中的密钥、接口地址和模型名称，并确认服务账号可用。截图识别还需要模型支持图片输入。

**缩小后找不到窗口？**  
窗口会缩为小型恢复按钮。点击它即可恢复；可通过 `[RestoreButton]` 调整按钮位置、大小和透明度。

**截图保存在哪里？**  
以 `[Screenshots] directory` 为准。新版发布包默认使用 `screenshots`；旧配置可能仍指向 `C:\a` 或其他位置。

<br>

## ⚠️ 注意事项

- 请联系联系作者以获得身份验证。
- 当前发布面向 **Windows x64**。
- 截图会保存到本地指定目录，可按需要自行管理。
