from preflibtools.instances import OrdinalInstance

def main():
    instance = OrdinalInstance()
    instance.parse_url("https://www.preflib.org/static/data/aspen/00016-00000001.toi")
    

if __name__ == "__main__":
    main()