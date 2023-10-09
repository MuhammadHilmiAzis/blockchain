import datetime
import hashlib
import json
from flask import Flask, jsonify, request

class Block:
    def __init__(self, index, data, previous_hash, proof_of_work=None):
        self.index = index
        self.timestamp = str(datetime.datetime.now())
        self.data = data
        self.previous_hash = previous_hash
        self.proof_of_work = proof_of_work
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data_str = json.dumps(self.data, sort_keys=True)
        return hashlib.sha256(
            (str(self.index) + self.timestamp + data_str + self.previous_hash + str(self.proof_of_work)).encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    def create_block(self, data):
        previous_block = self.get_last_block()
        proof = self.proof_of_work(previous_block.proof_of_work)
        new_block = Block(len(self.chain), data, previous_block.hash, proof)
        self.chain.append(new_block)

    def get_last_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 0
        while True:
            hash_operation = hashlib.sha256(
                (str(new_proof**2 - previous_proof**2)).encode()).hexdigest()
            if hash_operation[:self.difficulty] == '0' * self.difficulty:
                return new_proof
            new_proof += 1

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

            if not self.is_valid_proof(previous_block.proof_of_work, current_block.proof_of_work):
                return False

        return True

    @staticmethod
    def is_valid_proof(previous_proof, current_proof):
        guess = f'{previous_proof}{current_proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

app = Flask(__name__)

blockchain = Blockchain()

@app.route("/mine_block", methods=["GET"])
def mine_block():
    data = {"message": "Block mined successfully"}
    blockchain.create_block(data)
    return jsonify(data), 200

@app.route("/get_chain", methods=["GET"])
def get_chain():
    response = {
        "chain": [block.__dict__ for block in blockchain.chain],
        "length": len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route("/is_valid", methods=["GET"])
def is_valid():
    is_valid = blockchain.is_chain_valid()
    response = {"is_valid": is_valid}
    return jsonify(response), 200

@app.route("/add_data", methods=["POST"])
def add_data():
    data = request.json.get('data')
    blockchain.create_block(data)
    response = {"message": "Data added to a new block"}
    return jsonify(response), 201

@app.route("/modify_block", methods=["PUT"])
def modify_block():
    # Simulate modifying the last block in the chain
    if len(blockchain.chain) > 1:
        modified_data = "Modified Data"
        blockchain.chain[-1].data = modified_data
        response = {"message": "Block modified successfully"}
        return jsonify(response), 200
    else:
        response = {"message": "Cannot modify the genesis block"}
        return jsonify(response), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
