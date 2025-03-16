from argparse import ArgumentParser

import uvicorn


def run():
    uvicorn.run(
        f"{__package__}:create_app",
        factory=True,
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["src", "plugins"],
        log_config=None,
    )


parser = ArgumentParser()
parser.add_argument("action", choices=["run", "init"], default="run", nargs="?")
parser.add_argument("plugin", nargs="?")
args = parser.parse_args()

if args.action == "run":
    run()
if args.action == "init":
    from fairyjoke import app, plugin

    for p in plugin.load_plugins():
        if args.plugin and p.id != args.plugin:
            continue
        p.init()
