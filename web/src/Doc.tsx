import z from 'zod';
import './Doc.css'

export interface ResultDoc {
    /** The document ID */
    id: number,
    /** The Score returned by pylucene */
    score: number,
    /** The domain of the result */
    domain: string,
    /** The full URL of the result */
    url: string,
    /** The title of the webpage */
    title: string,
    /** All the image URLs in the site */
    images: string[],
    /** The parsed content */
    content: string,
}

const resultDocSchema = z.object({
    id: z.number().int(),
    score: z.number(),
    domain: z.string(),
    url: z.string().url(),
    title: z.string(),
    images: z.string().url().array(),
    content: z.string(),
})

export function isResultDoc(doc: unknown): doc is ResultDoc {
    const result = resultDocSchema.safeParse(doc);
    if (!result.success) {
        console.error(result.error);
        return false;
    } else {
        return true;
    }
}

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
