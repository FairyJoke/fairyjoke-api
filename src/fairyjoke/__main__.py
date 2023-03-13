from argparse import ArgumentParser

import uvicorn


def run():
    uvicorn.run(
        f"{__package__}:app",
        # factory=True,
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["src"],
    )


parser = ArgumentParser()
parser.add_argument("action", choices=["run"], default="run", nargs="?")
args = parser.parse_args()

if args.action == "run":
    run()
