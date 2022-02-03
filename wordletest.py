import subprocess
import re
from tqdm import tqdm

def wordle(answer, query):
    ret = ""
    for i in range(5):
        if query[i] == answer[i]:
            ret += "g"
        elif query[i] in answer:
            ret += "y"
        else:
            ret += "b"
    return ret

if __name__ == "__main__":
    print("Wordle Solver Test v0.1")
    success = 0
    failure = 0
    score_average = 0
    query_pattern = re.compile(r'[0-9] query: "(\w+)" \?')
    with open("wordlist.txt") as fp, open("solver_score.log", mode="w") as log:
        for w in tqdm(fp.readlines()):
            word = w.strip()
            proc = subprocess.Popen(["python", "main.py"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            dummy = proc.stdout.readline()
            for i in range(7):
                res = proc.stdout.read(19)
                if "success".encode("UTF-8") in res:
                    log.write(f"{word} success {i}\n")
                    success += 1
                    score_average += i
                    break
                elif "failure".encode("UTF-8") in res:
                    log.write(f"{word} failure\n")
                    failure += 1
                    break
                m = query_pattern.search(res.decode("UTF-8"))
                ret = wordle(word, m.group(1)) + "\r\n"
                proc.stdin.write(ret.encode("UTF-8"))
                proc.stdin.flush()
            proc.kill()
        score_average /= success
        log.write(f"\nsuccess {success}\nfailure {failure}\nscore_average {score_average}")
    print(f"success {success}\nfailure {failure}\nscore_average {score_average}\n")