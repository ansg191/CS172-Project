import {useEffect, useState} from 'react'
import Doc from "./Doc.tsx";
import './App.css'
import {isResultDoc, ResultDoc} from "./resultdoc.ts";

const group_members = [
    {name: "Anshul Gupta", sid: "862319580", nid: "agupt109"},
    {name: "Nikhil Mahendrakar", sid: "862464249", nid: "nmahe008"},
    {name: "Ishaan Bijor", sid: "862128714", nid: "ibijo001"},
    {name: "Junbo Yang", sid: "862234040", nid: "jyang389"},
    {name: "Junyan Hou", sid: "862394589", nid: "jhou038"},
]

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
            {data.length == 0 && query.length == 0 &&
                <div>
                    <h2 className="group-title">Group 10</h2>
                    <table className="group-table">
                        <tbody>
                        {group_members.map(member => <tr>
                            <td>{member.name}</td>
                            <td><a href={`mailto:${member.nid}@ucr.edu`}>{member.nid}</a></td>
                            <td>{member.sid}</td>
                        </tr>)}
                        </tbody>
                    </table>
                </div>
            }
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
