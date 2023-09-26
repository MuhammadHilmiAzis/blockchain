# import libraries

import datetime
import hashlib
import json
from flask import Flask, jsonify, request

# 1. Blockchain (Server)
class Blockchain:

    def __init__(self):
        self.chain = []
        # genesis block
        self.create_block(proof = 1, prev_hash = '0')

    def create_block(self, proof, prev_hash, proof_of_work=None, data=None):
        block = {
            'id_block': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'prev_hash': prev_hash,
            'proof_of_work': proof_of_work,
            'data': data
        }
        block['hash'] = self.get_hash(block)
        self.chain.append(block)
        return block

    def get_last_block(self):
        return self.chain[-1]

    def proof_of_work(self, prev_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof, hash_operation
    
    def get_hash(self, block):
        hash_operation = hashlib.sha256(json.dumps(block).encode()).hexdigest()
        return hash_operation
    
    def is_chain_valid(self):
        prev_block = self.chain[0]
        now_index = 1
        while counter < len(self.chain) + 1:
            now_block = self.chain[now_index]

            # 1. cek apakah hash now block = prev hash 
            prev_hash = self.get_hash(prev_block)
            if prev_hash != now_block['prev_hash']:
                return False

            # 2. cek apakah proof of worknya true
            now_proof = now_block['proof']
            prev_proof = prev_block['proof']
            hash_operation = hashlib.sha256(str(now_proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False

            prev_block = now_block
            now_index += 1
        return True

    def modify_block(self):
        pass


# 2. Web Aplikasi untuk Testing
app = Flask(__name__)

blockchain = Blockchain()

# buat endpoint 
@app.route("/get_chain", methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route("/mining", methods=['GET'])
def mining():
    prev_block = blockchain.get_last_block()
    # get prev proof 
    prev_proof = prev_block['proof']
    proof, proof_of_work = blockchain.proof_of_work(prev_proof) 
    # get prev hash 
    prev_hash = blockchain.get_hash(prev_block)
    # prev_hash = prev_block['hash']
    # create block 
    created_block = blockchain.create_block(proof, prev_hash, proof_of_work)
    response = {
        'message': "Blockchain is successfully created",
        'created block': created_block
    }
    return jsonify(response), 200


@app.route("/create", methods=['POST'])
def create_block():
    data = request.form

    prev_block = blockchain.get_last_block()
    # get prev proof 
    prev_proof = prev_block['proof']
    proof, proof_of_work = blockchain.proof_of_work(prev_proof) 
    # get prev hash 
    prev_hash = blockchain.get_hash(prev_block)
    # create block 
    created_block = blockchain.create_block(proof, prev_hash, proof_of_work, data['data'])
    response = {
        'message': "Blockchain is successfully created",
        'created block': created_block
    }
    return jsonify(response), 200

from flask import Flask, request, jsonify

app = Flask(__name__)

class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Implementasikan algoritma hash (misalnya, SHA-256)
        # Anda dapat menggunakan pustaka seperti hashlib untuk ini
        return "hashed_value"

# Inisialisasi blockchain dengan blok awal
blockchain = [Block(0, "Genesis Block", "0")]

# Fungsi untuk menambahkan blok baru ke blockchain
def add_block(data):
    previous_block = blockchain[-1]
    new_index = previous_block.index + 1
    new_block = Block(new_index, data, previous_block.hash)
    blockchain.append(new_block)

# Fungsi untuk memeriksa validitas blockchain
def is_valid_blockchain():
    for i in range(1, len(blockchain)):
        current_block = blockchain[i]
        previous_block = blockchain[i - 1]
        # Periksa apakah hash sebelumnya sesuai dengan hash blok sebelumnya
        if current_block.previous_hash != previous_block.hash:
            return False
    return True

# Endpoint untuk menambahkan blok ke blockchain
@app.route('/add_block', methods=['POST'])
def add_new_block():
    data = request.json.get('data')
    add_block(data)
    return "Block added successfully"

# Endpoint untuk memeriksa validitas blockchain
@app.route('/check_validity', methods=['GET'])
def check_validity():
    is_valid = is_valid_blockchain()
    if is_valid:
        return "Blockchain is valid"
    else:
        return "Blockchain is not valid"
    
    
app.run()

# Tugas 
# 1. Buatkan endpoint yang mengecek apakah chainnya valid
# 2. Simpan hash block didalam blocknya
# 3. Tambah data diddalam block
# 4. Fungsi dan endpoint yang mensimulasikan adanya modifikasi didalam block, sehingga chainnya tidak valid
