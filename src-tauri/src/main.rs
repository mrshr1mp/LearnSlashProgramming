// The installed app: a real window around the same Python app you run with Start Learning.bat.
// It starts the bundled Python (app/app.py) in the background, shows a loading screen until it answers,
// then opens it. Your code and progress live in your user folder, so updates never touch them.
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")] // no console window

use std::net::TcpStream;
use std::path::PathBuf;
use std::process::{Child, Command};
use std::sync::Mutex;
use std::time::Duration;
use tauri::{AppHandle, Manager, RunEvent, Url, WebviewUrl, WebviewWindowBuilder};
use tauri_plugin_dialog::{DialogExt, MessageDialogButtons};
use tauri_plugin_updater::UpdaterExt;

const PORT: u16 = 8790; // not 8765, so it never fights with a copy run from the code folder

struct Server(Mutex<Option<Child>>);

fn python(resources: &PathBuf) -> PathBuf {
    if cfg!(windows) {
        resources.join("python").join("pythonw.exe") // bundled with the installer
    } else {
        PathBuf::from("python3") // every Linux has it
    }
}

fn start_server(app: &AppHandle) -> Result<Child, String> {
    let resources = app.path().resource_dir().map_err(|e| e.to_string())?;
    let data = app.path().app_data_dir().map_err(|e| e.to_string())?;
    std::fs::create_dir_all(&data).map_err(|e| e.to_string())?;
    let mut cmd = Command::new(python(&resources));
    cmd.arg(resources.join("app").join("app.py"))
        .arg("--no-window")
        .current_dir(&data)
        .env("LEARN_HOME", &data)
        .env("LEARN_PORT", PORT.to_string())
        .env("LEARN_VERSION", app.package_info().version.to_string())
        .env_remove("PYTHONHOME")
        .env_remove("PYTHONPATH");
    #[cfg(windows)]
    {
        use std::os::windows::process::CommandExt;
        cmd.creation_flags(0x0800_0000); // CREATE_NO_WINDOW
    }
    cmd.spawn().map_err(|e| format!("Couldn't start Python: {e}"))
}

fn stop_server(app: &AppHandle) {
    if let Some(mut child) = app.state::<Server>().0.lock().unwrap().take() {
        let _ = child.kill();
    }
}

async fn check_for_update(app: AppHandle) -> tauri_plugin_updater::Result<()> {
    let handle = app.clone();
    let updater = app.updater_builder().on_before_exit(move || stop_server(&handle)).build()?;
    if let Some(update) = updater.check().await? {
        let yes = app
            .dialog()
            .message(format!("Version {} is ready. Update now? The app restarts by itself.", update.version))
            .title("Update available")
            .buttons(MessageDialogButtons::OkCancelCustom("Update now".into(), "Later".into()))
            .blocking_show();
        if yes {
            update.download_and_install(|_, _| {}, || {}).await?;
            stop_server(&app);
            app.restart();
        }
    }
    Ok(())
}

fn main() {
    let app = tauri::Builder::default()
        .plugin(tauri_plugin_single_instance::init(|app, _, _| {
            // opened it twice: just bring the window back
            if let Some(w) = app.get_webview_window("main") {
                let _ = w.unminimize();
                let _ = w.set_focus();
            }
        }))
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_updater::Builder::new().build())
        .manage(Server(Mutex::new(None)))
        .setup(|app| {
            let window = WebviewWindowBuilder::new(app, "main", WebviewUrl::App("index.html".into()))
                .title("learn/programming")
                .inner_size(1280.0, 900.0)
                .min_inner_size(800.0, 600.0)
                .build()?;
            let started = start_server(app.handle());
            let ok = started.is_ok();
            if let Ok(child) = started {
                *app.state::<Server>().0.lock().unwrap() = Some(child);
            }
            std::thread::spawn(move || {
                // wait for Python to answer (usually under a second), then show the app
                for _ in 0..if ok { 150 } else { 5 } {
                    if TcpStream::connect(("127.0.0.1", PORT)).is_ok() {
                        let _ = window.navigate(Url::parse(&format!("http://127.0.0.1:{PORT}/")).unwrap());
                        return;
                    }
                    std::thread::sleep(Duration::from_millis(100));
                }
                let _ = window.eval("document.body.classList.add('failed')");
            });
            let handle = app.handle().clone();
            tauri::async_runtime::spawn(async move {
                let _ = check_for_update(handle).await; // offline or GitHub down: try again next launch
            });
            Ok(())
        })
        .build(tauri::generate_context!())
        .expect("couldn't start learn/programming");
    app.run(|handle, event| {
        if let RunEvent::Exit = event {
            stop_server(handle);
        }
    });
}
