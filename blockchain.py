from hashlib import sha256

def updatehash(*args):
    hashingText = ""; h = sha256()
    for arg in args:
        hashingText += str(arg)

    h.update(hashingText.encode('utf-8'))
    return h.hexdigest()


class Block():
    data = None
    hash = None
    nonce = 0
    prevHash = "0" * 64

    def __init__(self,data,number=0): # Genesis block
        self.data = data
        self.number = number

    def hash(self):
        return updatehash(self.prevHash, self.number, self.data, self.nonce)

    def __str__(self):
        return str("Block#: %s\nHash: %s\nPrevious Hash: %s\nData: %s\nNonce: %s\n"%(
                self.number,
                self.hash(),
                self.prevHash,
                self.data,
                self.nonce
            ))



class Blockchain():
    difficulty = 3

    # @notice Initilazing the first block of the chain 
    # @param Setting chain as a variable
    def __init__(self,chain=[]):
        self.chain = chain

    # @notice Creating new blocks
    # @param Taking the block class variables
    def create(self, block):
        self.chain.append(block)

    def remove(self, block):
        self.chain.remove(block)

    # @notice Mining the blocks
    # @param Taking the block class variables
    def mine(self, block):
        try:    
            block.prevHash = self.chain[-1].hash()
        except IndexError:
            pass

        while True:
            if block.hash()[:self.difficulty] == "0" * self.difficulty:
                self.create(block); break
            else:
                block.nonce += 1

    # @notice Checking the validity of blockchain
    # @return The validity of the blockchain
    def isValid(self):
        for i in range(1,len(self.chain)):
            _previous = self.chain[i].prevHash
            _current = self.chain[i-1].hash()
            
            if _current == _previous or _current[:self.difficulty] == "0" * self.difficulty:
                return True
            else:
                return False






def main():
    # Defining blockchain variable
    blockchain = Blockchain()
    database = ["hello world","what","hello","bye"]

    num = 0
    for data in database:
        num += 1
        blockchain.mine(Block(data,num))

    for block in blockchain.chain:
        print(block)

    print(blockchain.isValid())

if __name__ == '__main__':
    main()
