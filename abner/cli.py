import sys


def main():
    if len(sys.argv) != 2 or sys.argv[1] != "start":
        print("Usage: abner start")
        sys.exit(1)

    # Import and run the GUI
    try:
        from abner.GUIs.GUI_ABNER import run_gui
    except ImportError as e:
        print(f"Error: Could not start ABNER GUI: {e}")
        sys.exit(1)

    run_gui()


if __name__ == "__main__":
    main()
