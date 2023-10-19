from argparse import ArgumentParser

import uvicorn


def run():
    uvicorn.run(
        f"{__package__}:app",
        # factory=True,
        host=host,
        port=port,
        reload=True,
        reload_dirs=["src"],
    )


parser = ArgumentParser()
parser.add_argument("action", choices=["run"], default="run", nargs="?")
args = parser.parse_args()
host = "0.0.0.0"
port = 8000

if args.action == "run":
    run()
