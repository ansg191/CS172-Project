import './Doc.css'
import {ResultDoc} from "./resultdoc.ts";

export interface DocParams {
    document: ResultDoc,
}

function Doc({document}: DocParams) {
    return (
        <div className="card">
            <div className="card-body">
                <h2 className='doc-title'>
                    <a href={document.url} target="_blank" rel="noreferrer noopener">
                        {document.title}
                    </a>
                </h2>
                <div className='doc-domain-score'>
                    <p className='doc-domain'>{document.domain}</p>
                    <p className='doc-domain'>Score: {(document.score).toFixed(2)}</p>
                </div>
            </div>
        </div>
    )
}

export default Doc;
