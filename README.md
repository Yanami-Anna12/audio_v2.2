# 综合重启工具

## 说明
- [ ] 打包成exe的命令，进入代码根目录，使用命令:pyinstaller  -D -w -i  .\wav.ico -p C:\Windows\System32\downlevel .\frame_to_wav_run.py 或 py -3.9 -m PyInstaller .\frame_to_wav_run.spec
- [ ] myconfig.yml文件为可配置文件，可对一些参数做修改，位置为\get_data\base
- [ ] 资源文件如果要打包，则在*.spec文件中datas行，替换内容为： datas=[('get_data','get_data')],