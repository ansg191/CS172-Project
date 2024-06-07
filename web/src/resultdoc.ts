import z from "zod";

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
    url: z.string(),
    title: z.string(),
    images: z.string().array(),
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
