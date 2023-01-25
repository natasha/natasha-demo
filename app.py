
from os import getenv
import logging

import sys
from io import StringIO
from contextlib import contextmanager

from aiohttp import web
from aiohttp_cors import (
    ResourceOptions,
    setup as setup_cors
)

from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    PER,
    NamesExtractor,

    Doc
)


HOST = getenv('HOST', '0.0.0.0')
PORT = int(getenv('PORT', 4000))

CORS = {
    '*': ResourceOptions(
        allow_credentials=True,
        expose_headers='*',
        allow_headers='*',
    )
}


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)-15s %(message)s'
)
log = logging.info


def cap_text(text, cap=5000):  # 99.9% lenta.ru articles < 5000 symbols
    return text[:cap]


class Processor:
    def __init__(self):
        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()

        self.emb = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(self.emb)
        self.syntax_parser = NewsSyntaxParser(self.emb)
        self.ner_tagger = NewsNERTagger(self.emb)

        self.names_extractor = NamesExtractor(self.morph_vocab)

    def __call__(self, text):
        doc = Doc(text)
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)
        doc.parse_syntax(self.syntax_parser)
        doc.tag_ner(self.ner_tagger)

        for token in doc.tokens:
            token.lemmatize(self.morph_vocab)

        for span in doc.spans:
            span.normalize(self.morph_vocab)
            if span.type == PER:
                span.extract_fact(self.names_extractor)

        return doc


async def doc_spans(request):
    form = await request.post()
    text = cap_text(form['text'])

    doc = request.app['processor'](text)

    for span in doc.spans:
        span.tokens = None

    data = [_.as_json for _ in doc.spans]

    log(text)
    return web.json_response(data)


@contextmanager
def capture():
    stdout = sys.stdout
    buffer = StringIO()
    sys.stdout = buffer
    yield buffer
    sys.stdout = stdout


async def doc_viz(request):
    form = await request.post()
    text = cap_text(form['text'])

    doc = request.app['processor'](text)
    data = {}

    with capture() as buffer:
        doc.ner.print()
        data['ner'] = buffer.getvalue()

    if doc.sents:
        sent = doc.sents[0]

        with capture() as buffer:
            sent.morph.print()
            data['morph'] = buffer.getvalue()

        with capture() as buffer:
            sent.syntax.print()
            data['syntax'] = buffer.getvalue()

        for span in doc.spans:
            span.tokens = None

        data['spans'] = [_.as_json for _ in doc.spans]

    log(text)
    return web.json_response(data)


def init():
    app = web.Application()
    app['processor'] = Processor()

    cors = setup_cors(app, defaults=CORS)
    cors.add(app.router.add_route('POST', '/api/doc/spans', doc_spans))
    cors.add(app.router.add_route('POST', '/api/doc/viz', doc_viz))

    return app


if __name__ == '__main__':
    app = init()
    web.run_app(app, host=HOST, port=PORT)
