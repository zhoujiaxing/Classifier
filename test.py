import mongocli
import json
if __name__ == "__main__":
	client=mongocli.MongoCli()
	datas=client.getdata('hinews','article',1)
