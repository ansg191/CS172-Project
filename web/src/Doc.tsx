import './Doc.css'
import {ResultDoc} from "./resultdoc.ts";

export interface DocParams {
    document: ResultDoc,
}

function Doc({document}: DocParams) {
    return (
        <div className="card">
            <div className="card-body">
                <div className="image-container">
                    <img className="image" src={document.images[0]} alt={document.title}/>
                </div>
                <div className="doc-text">
                    <h2 className='doc-title'>
                        <a href={document.url} target="_blank" rel="noreferrer noopener">
                            {document.title}
                        </a>
                    </h2>
                    <div className='doc-domain-score'>
                        <p className='doc-domain'>{document.domain}</p>
                        <p className='doc-domain'>Score: {(document.score).toFixed(2)}</p>
                    </div>
                    <p className='doc-content'>
                        {document.content}
                    </p>
                </div>
            </div>
        </div>
    )
}

export default Doc;
