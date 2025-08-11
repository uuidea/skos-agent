# run.py

import sys
from skos_agent.graph import create_agent

def main():
    if len(sys.argv) != 2:
        print("Usage: python run.py <document_path>")
        sys.exit(1)

    doc_path = sys.argv[1]
    agent = create_agent()
    result = agent.invoke({"file_path": doc_path})
    print(result)

if __name__ == "__main__":
    main()