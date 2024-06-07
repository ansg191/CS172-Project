import csv
import sys
import lucene

from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, TextField, StoredField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader
from org.apache.lucene.store import NIOFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.queryparser.classic import QueryParser


INDEX_PATH = "index/"
CSV_PATH = "computerscience_data.csv"

initialized = False

csv.field_size_limit(sys.maxsize)


class Index:
    def __init__(self):
        self.init()
        self.analyzer = StandardAnalyzer()
        self.dir = NIOFSDirectory(Paths.get(INDEX_PATH))

    def init(self):
        global initialized
        if not initialized:
            lucene.initVM()
            initialized = True

    def read_csv(self):
        rows = []
        with open(CSV_PATH) as csvfile:
            reader = csv.reader(csvfile)
            rows = [row for row in reader]
        return rows

    def has_data(self):
        try:
            reader = DirectoryReader.open(self.dir)
            ret = reader.numDocs() > 0
            reader.close()
            return ret
        except Exception as e:
            return False

    def build_index(self):
        self.init()
        if self.has_data():
            return

        print("Building Index...")
        writerConfig = IndexWriterConfig(StandardAnalyzer())
        writer = IndexWriter(self.dir, writerConfig)

        rows = self.read_csv()

        for i in range(1, len(rows)):
            if i % 100 == 0:
                print(f"Processing {i}/{len(rows)}")

            doc = Document()
            doc.add(TextField("domain", rows[i][0], Field.Store.YES))
            doc.add(TextField("title", rows[i][1], Field.Store.YES))
            doc.add(TextField("content", rows[i][2], Field.Store.YES))
            doc.add(StoredField("images", rows[i][3]))
            doc.add(StoredField("url", rows[i][4]))
            writer.addDocument(doc)

        writer.close()

    def query(self, query):
        # Attach current thread to JVM
        lucene.getVMEnv().attachCurrentThread()

        reader = DirectoryReader.open(self.dir)
        print(reader.numDocs())
        searcher = IndexSearcher(reader)
        parser = QueryParser("content", self.analyzer)
        q = parser.parse(query)
        hits = searcher.search(q, 10)

        results = []
        for hit in hits.scoreDocs:
            doc = searcher.doc(hit.doc)

            results.append(
                {
                    "score": hit.score,
                    "id": hit.doc,
                    "domain": doc.get("domain"),
                    "title": doc.get("title"),
                    "content": doc.get("content"),
                    "images": doc.get("images").split("|"),
                    "url": doc.get("url"),
                }
            )

        return results
