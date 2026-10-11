using System;
using System.Text;
using System.Runtime.InteropServices;
using System.Runtime.InteropServices.ComTypes;
namespace OmniView {
  [ComImport, Guid("00021401-0000-0000-C000-000000000046")] internal class ShellLink {}
  [ComImport, Guid("000214F9-0000-0000-C000-000000000046"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
  internal interface IShellLinkW {
    void GetPath([Out, MarshalAs(UnmanagedType.LPWStr)] StringBuilder path, int count, IntPtr data, uint flags);
    void GetIDList(out IntPtr pidl); void SetIDList(IntPtr pidl);
    void GetDescription([Out, MarshalAs(UnmanagedType.LPWStr)] StringBuilder text, int count);
    void SetDescription([MarshalAs(UnmanagedType.LPWStr)] string text);
    void GetWorkingDirectory([Out, MarshalAs(UnmanagedType.LPWStr)] StringBuilder path, int count);
    void SetWorkingDirectory([MarshalAs(UnmanagedType.LPWStr)] string path);
    void GetArguments([Out, MarshalAs(UnmanagedType.LPWStr)] StringBuilder text, int count);
    void SetArguments([MarshalAs(UnmanagedType.LPWStr)] string text);
    void GetHotkey(out short hotkey); void SetHotkey(short hotkey);
    void GetShowCmd(out int command); void SetShowCmd(int command);
    void GetIconLocation([Out, MarshalAs(UnmanagedType.LPWStr)] StringBuilder path, int count, out int index);
    void SetIconLocation([MarshalAs(UnmanagedType.LPWStr)] string path, int index);
    void SetRelativePath([MarshalAs(UnmanagedType.LPWStr)] string path, uint reserved);
    void Resolve(IntPtr hwnd, uint flags);
    void SetPath([MarshalAs(UnmanagedType.LPWStr)] string path);
  }
  public class ShortcutDetails {
    public string Target {get;set;} public string Arguments {get;set;}
    public string WorkingDirectory {get;set;} public string Icon {get;set;}
    public int IconIndex {get;set;}
  }
  public static class NativeShortcut {
    public static void Create(string destination, string target, string arguments, string directory, string icon, string description) {
      object instance=new ShellLink();
      try {
        IShellLinkW link=(IShellLinkW)instance;
        link.SetPath(target);link.SetArguments(arguments);link.SetWorkingDirectory(directory);
        link.SetIconLocation(icon,0);link.SetDescription(description);
        ((IPersistFile)instance).Save(destination,true);
      } finally {Marshal.FinalReleaseComObject(instance);}
    }
    public static ShortcutDetails Read(string source) {
      object instance=new ShellLink();
      try {
        ((IPersistFile)instance).Load(source,0);
        IShellLinkW link=(IShellLinkW)instance;
        StringBuilder target=new StringBuilder(32768),arguments=new StringBuilder(32768),directory=new StringBuilder(32768),icon=new StringBuilder(32768);
        int index;
        link.GetPath(target,target.Capacity,IntPtr.Zero,0);
        link.GetArguments(arguments,arguments.Capacity);link.GetWorkingDirectory(directory,directory.Capacity);
        link.GetIconLocation(icon,icon.Capacity,out index);
        return new ShortcutDetails {Target=target.ToString(),Arguments=arguments.ToString(),WorkingDirectory=directory.ToString(),Icon=icon.ToString(),IconIndex=index};
      } finally {Marshal.FinalReleaseComObject(instance);}
    }
  }
}
