import okKey

import os
import json
from datetime import datetime, timedelta
import base64

class okBlock(object):
    def __init__(self):
        self.previousHash = " "
        self.blockBody = [   {
                                    'sender': "atThe",
                                    'recipient': "Beginning",
                                    'contents': "LetThereBeLight",
                                    'note': "noTransactionsOnGenesisBlock"
                                } ]

    def addBlock(self, preBlkHash):
        self.previousHash = preBlkHash
        blockHead = {
            'previousHash' : preBlkHash,
            'blockBody' : self.blockBody
        }
        notify = self.blockBody
        self.blockBody = []
        return blockHead, \
            base64.b64encode(
                okKey.getHash(
                    json.dumps(blockHead,
                        ensure_ascii=False, sort_keys=True).encode())).decode()

    def addTransaction(self, sender, recipient, contents, note):
        transaction = {
                        'sender': sender,
                        'recipient': recipient,
                        'contents': contents,
                        'note': note
        }
        self.blockBody.append(transaction)
        return base64.b64encode(
            okKey.getHash(
                json.dumps(transaction,
                    ensure_ascii=False, sort_keys=True).encode())).decode()


class okNode(object):
    def __init__(self):
        self.waitingList = {}
        self.blockList = []
        self.blockChain = {}
        self.myBlock = okBlock()
        self.previousBlockHash = \
            base64.b64encode(okKey.getHash(os.urandom(64))).decode()
        self.addBlock()

    @property
    def block(self):
        return self.myBlock

    def addBlock(self):
        blockHead, currentBlockHash = self.myBlock.addBlock(self.previousBlockHash)
        self.previousBlockHash = currentBlockHash
        self.blockList.append(blockHead)
        self.blockChain[currentBlockHash] = blockHead # file mapping
        for fixedTransaction in blockHead['blockBody']:
            tID = base64.b64encode(
                okKey.getHash(
                    json.dumps(fixedTransaction,
                        ensure_ascii=False, sort_keys=True).encode())).decode()
            if tID in self.waitingList:
                self.waitingList[tID]['blockHash'] = currentBlockHash
            else:
                if fixedTransaction['note'] != "noTransactionsOnGenesisBlock":
                    print('error #1004')
        return currentBlockHash

    def depositTransaction(self, sender, recipient, contents, note):
        tID = self.block.addTransaction(sender, recipient, contents, note)
        # print('deposit tID {0}'.format(tID))
        self.waitingList[tID] = {'sender' : sender, 'blockHash' : ' '}
        return tID

    def vouchHash(self, tID):
        # print('Vouch tID: {0}'.format(tID))
        # print(self.waitingList)
        if tID in self.waitingList.keys():
            if self.waitingList[tID]['blockHash'] != ' ':
                waiting = self.waitingList.pop(tID)
                return waiting['blockHash']
            else:
                return 'Not approved'
        return 'Invalid Transactiom ID'

    def dumpBlocks(self):
        myBlock = { "Block Cahin" : self.blockChain }
        return json.dumps(myBlock)

    def dumpList(self):
        myBlock = { "Block List" : self.blockList }
        return json.dumps(myBlock)

    def dumpWaitingList(self):
        myBlock = { "Waiting List" : self.waitingList }
        return json.dumps(myBlock)

# error #1004 : unknown transaction on notification


class colleague(object):
    def __init__(self):
        self.key = okKey.getKey()
        self.ID = okKey.getPubID(self.key)
        self.waitingList = []
        self.history = {}

    @property
    def id(self):
        return self.ID

    def getDepositID(self, voucher):
        self.waitingList.append(voucher)

    def getVoucher(self, node):
        message = ['Not approved', 'Invalid Transactiom ID']
        for tID in self.waitingList:
            hash = node.vouchHash(tID)
            #print('voucher handler tID: {0} BlockHash: {1}'.format(tID, hash))
            if hash not in message:
                self.history[tID] = hash
                self.waitingList.remove(tID)

    def dumpList(self):
        wList = { "Colleague ID": self.ID,
                "Colleague Waiting List" : self.waitingList }
        return json.dumps(wList)

    def dumpHistory(self):
        hList = { "Colleague ID": self.ID,
                "Transaction History" : self.history }
        return json.dumps(hList)

# error #3003 :


if __name__ == '__main__':
    myNode = okNode()
    print(myNode.dumpBlocks())
    print(myNode.dumpList())

    aColleague = colleague()
    bColleague = colleague()
    cColleague = colleague()

    aColleague.getDepositID(myNode.depositTransaction(
                    aColleague.id, bColleague.id, "with love", "letter"))
    aColleague.getDepositID(myNode.depositTransaction(
                    aColleague.id, cColleague.id, "with", "head"))
    bColleague.getDepositID(myNode.depositTransaction(
                    bColleague.id, cColleague.id, "me", "you"))
    print(aColleague.dumpList())
    print(bColleague.dumpList())
    print(cColleague.dumpList())
    print(myNode.dumpWaitingList())
    myNode.addBlock() # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    print(myNode.dumpBlocks())
    aColleague.getVoucher(myNode)
    bColleague.getVoucher(myNode)
    cColleague.getVoucher(myNode)
    print(aColleague.dumpHistory())
    print(bColleague.dumpHistory())
    print(cColleague.dumpHistory())

    cColleague.getDepositID(myNode.depositTransaction(
                    cColleague.id, aColleague.id, "from me", "to you"))
    cColleague.getDepositID(myNode.depositTransaction(
                    cColleague.id, bColleague.id, "with love", "none"))
    print(aColleague.dumpList())
    print(bColleague.dumpList())
    print(cColleague.dumpList())
    myNode.addBlock() # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    print(myNode.dumpBlocks())
    aColleague.getVoucher(myNode)
    bColleague.getVoucher(myNode)
    cColleague.getVoucher(myNode)
    print(aColleague.dumpHistory())
    print(bColleague.dumpHistory())
    print(cColleague.dumpHistory())
