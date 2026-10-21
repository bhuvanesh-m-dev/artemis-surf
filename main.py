"""ArtemisSurf entry point:  python main.py"""
import bootstrap


def main():
    bootstrap.ensure_ready()
    from artemis.app import run
    run()


if __name__ == "__main__":
    main()
