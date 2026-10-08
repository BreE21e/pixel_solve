# pixel_solve：数字轰炸，CTF 像素画还原

使用 Python 和 Pillow，把题目中连续 9 天收到的数字还原为黑白像素画，并生成完整图片和带网格的分段图片。**脚本只负责画图，flag 需要打开图片后人工读出，不会自动识别或打印 flag。**

## 1. 准备文件与安装依赖

下载本仓库：在 GitHub 仓库页面点击 **Code → Download ZIP**，然后解压。已有 Git 的用户也可以运行：

```bash
git clone https://github.com/BreE21e/pixel_solve.git
cd pixel_solve
```

仓库中的文件是：

- `README.md`：本说明。
- `pixel_solve.py`：脚本，已经内置本题完整的 9 行坐标数据。

需要 Python 3 和第三方库 **Pillow**。安装时使用库名 `Pillow`，代码中通过 `from PIL import Image, ImageDraw` 导入。

Windows：在解压后的项目文件夹中打开 PowerShell 或 CMD，运行：

```powershell
py -3 --version
py -3 -m pip install Pillow
```

macOS / Linux：在项目文件夹中打开终端，运行：

```bash
python3 --version
python3 -m pip install Pillow
```

如果使用虚拟环境，请在激活环境后用 `python -m pip install Pillow` 安装，再用同一个 `python` 运行脚本。安装依赖和运行脚本必须使用同一个 Python 环境。

## 2. 输入数据放在哪里

**复现原题无需另建输入文件，也无需修改脚本。** 全部输入已经放在 `pixel_solve.py` 开头的 `data = '''...'''` 多行字符串中。

当前脚本没有命令行参数，也不会读取 `data.txt`。把文件名写在命令后面（例如 `python3 pixel_solve.py data.txt`）不会切换输入；脚本仍然使用内置数据。

需要替换坐标时，编辑 `data` 的三引号内部，按以下格式填写：

- 一行对应一天，按第 1 天到第 9 天的顺序排列。
- 每行至少包含一个非负十进制整数，用空格或制表符分隔。
- 不要添加逗号、括号、“第 1 天”等标签或注释。
- 不要插入空行；三引号内开头和中间的空行都会导致空集合参与求最大值而报错。
- 横坐标从 `0` 开始。数字不必排序，同一行的重复数字会被集合自动去重。
- 本题数据共有 9 行，坐标范围为 `0..146`，最大值为 `146`。

下面是**格式演示数据，不是原题数据，不会生成原题 flag**。替换时保留三引号，让第一个数字紧跟在开头三引号后：

```python
data = '''0 2 4
1 3
0 4
1 3
0 2 4
1 3
0 4
1 3
0 146'''
```

完整图片的逻辑宽度自动取“全部坐标的最大值 + 1”，高度取输入行数。分段网格则写死了 `0..48`、`49..97`、`98..146` 三段和固定画布大小，按本题 9 行设计；它不会随新数据自动扩展。其他题目若超过 146 列坐标范围或超过 9 行，需调整分段范围、画布和段间距，否则分段图可能漏画、重叠或裁切。负数也没有校验，请不要输入负坐标。

## 3. 运行脚本

在包含 `pixel_solve.py` 的项目文件夹中运行。

Windows：

```powershell
py -3 pixel_solve.py
```

macOS / Linux：

```bash
python3 pixel_solve.py
```

使用未修改的原题数据，运行成功后终端显示：

```text
Rendered 147 columns and 9 rows
```

脚本不会自动弹出图片窗口。请到输出目录中打开下面两张 PNG。

## 4. 输出图片在哪里

**输出保存到终端的当前工作目录，不一定是脚本所在目录。** 按上面的步骤先进入项目文件夹，两张图就会出现在 `pixel_solve.py` 旁边。若在其他目录用脚本的绝对路径运行，图片会出现在那个工作目录中。

| 文件 | 原题数据的图片大小 | 内容 |
| --- | --- | --- |
| `pixel_flag.png` | 1764 × 108 像素 | 完整黑白像素画；147 列 × 9 行，每个逻辑像素放大为 12 × 12 像素 |
| `pixel_grid.png` | 1000 × 650 像素 | 带浅灰网格的三段图片；每格占 19 × 19 像素，方便看清字符 |

读取 `pixel_grid.png` 时，按**上段 → 中段 → 下段**拼接字符，分别对应横坐标 `0..48`、`49..97`、`98..146`；每段中的第 1 天都在最上面。

每次运行都会覆盖当前目录里同名的两张图片。需要保留旧结果时，请先复制或重命名。

## 5. 解题思路

结合“像素画”“坐标轴”和“方格”的提示，把每个数字当作一列的位置，把每天的数据当作一行：

- 第 1 天的数据放在最上面，第 9 天的数据放在最下面。
- 某个数字出现，就将对应位置涂黑；没有出现的位置保持白色。
- 使用图片坐标：原点在左上角，横坐标向右增加，行号向下增加。

例如，第 1 天包含 `25 31 32`，就将最上面一行中横坐标为 25、31、32 的方格涂黑。程序行编号从 0 开始，因此对应 `(25, 0)`、`(31, 0)`、`(32, 0)`。

本题最大数字为 146，因此需要 147 列；共有 9 天，因此需要 9 行。填完方格后，黑块会组成字符，打开图片即可尝试读出 flag。

## 6. 常见错误

| 现象或报错 | 原因与处理 |
| --- | --- |
| `py` 或 `python3` 未被识别 | 尚未安装 Python，或命令不在 PATH 中。Windows 若已有 `python` 命令，可把安装、运行示例都改用 `python`，先用 `python --version` 确认是 Python 3。 |
| `ModuleNotFoundError: No module named 'PIL'` | Pillow 没有装在当前运行脚本的 Python 环境中。使用同一个解释器执行 `-m pip install Pillow`；不要安装名为 `PIL` 的包。 |
| `No module named pip` | 当前解释器没有 pip。可先用同一解释器运行 `-m ensurepip --upgrade`；若系统不提供 ensurepip，按该 Python 发行版的方式安装 pip。 |
| 安装时报 `externally-managed-environment` | 在支持 venv 的 Python 中创建虚拟环境：`python3 -m venv .venv`，激活后用 `python -m pip install Pillow` 和 `python pixel_solve.py`。macOS / Linux 激活命令为 `source .venv/bin/activate`。 |
| `can't open file ... pixel_solve.py` | 当前目录不含脚本，或脚本路径错误。先进入下载并解压后的项目目录；文件夹路径含空格时加引号。 |
| `ValueError: invalid literal for int()` | 数据中混入了逗号、文字等非整数内容。每行只保留以空白分隔的整数。 |
| `ValueError: max() arg is an empty sequence` | `data` 为空，或包含空行 / 只有空白字符的行。确保至少一行，每行至少一个整数。 |
| `PermissionError` | 当前工作目录不可写，或输出文件不可覆盖。进入可写目录后重试，并检查同名文件权限。 |
| 显示成功但找不到图片 | 检查终端当前工作目录：PowerShell 用 `Get-Location`，CMD 用 `cd`，macOS / Linux 用 `pwd`。脚本不会自动打开图片。 |
| 图片有了，但终端没有 flag | 这是正常行为：程序只打印行列数，需要打开图片人工读出字符。 |
| 修改数据后分段图缺少字符或重叠 | 分段范围和画布是为本题固定的。先检查完整图，再按新数据调整分段绘图代码。 |
