import {useEffect, useState} from 'react'
import Doc from "./Doc.tsx";
import './App.css'
import {isResultDoc, ResultDoc} from "./resultdoc.ts";

function App() {
    const [query, setQuery] = useState('');
    const [data, setData] = useState<ResultDoc[]>([]);

    useEffect(() => {
        if (query.length == 0) {
            setData([]);
            return;
        }

        fetch(`/query?q=${query}`, {
            method: "GET"
        })
            .then(res => res.json())
            .then((data: unknown) => {
                if (Array.isArray(data) && data.every(isResultDoc)) {
                    setData(data);
                } else {
                    console.error("Retrieved data is invalid");
                }
            })
    }, [query]);

    return (
        <>
            <h1>CS172 Project</h1>
            <div className="card">
                <input className="searchbox" type="text" value={query} onChange={(e) => setQuery(e.target.value)}/>
                {/*Add this later if search becomes too long*/}
                {/*<button id="searchbutton" type="submit">*/}
                {/*    Search!*/}
                {/*</button>*/}
            </div>

            <div className="item-container">
                {data.map((doc: ResultDoc) => <Doc document={doc} key={doc.id}/>)}
                {data.length == 0 && query.length > 0 &&
                    <div className="card">
                        <p>No Results Found</p>
                    </div>
                }
            </div>
        </>
    )
}

export default App
