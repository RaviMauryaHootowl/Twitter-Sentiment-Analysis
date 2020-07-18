import React, {useState, useEffect} from 'react';
import logo from  '../../assets/logo.png';
import './Home.css';

const Home = () => {
  const [search, setSearch] = useState("");
  const [percent, setPercent] = useState(0.0);
  const [isLoading, setIsLoading] = useState(false);
  const [fillColor , setFillColor] = useState('#39F082');

  const onSearch = () => {
    setIsLoading(true);
    console.log("Searching...");
    fetch(`http://127.0.0.1:5000/api/v1/search?query=${search}`).then(res => res.json())
    .then((result) => {setPercent(parseFloat(result['percent'])); 
      if(parseFloat(result['percent']) < 30) {setFillColor("#e74c3c")}
      else if(parseFloat(result['percent']) < 60) {setFillColor("#e67e22")}
      else { setFillColor("#2ecc71")}
      setIsLoading(false);
    })
    .catch((e) => {setIsLoading(false);})
  }

  return (
    <div className="homePage">
      <img className="logoImage" src={logo} alt=""/>
      <input onKeyDown={(e) => { if(e.key === 'Enter'){onSearch();}}} className="searchInput" value={search} onChange={(e) => {setSearch(e.target.value)}} type="text" placeholder="Search a topic"/>
      <div className="bottomContainer">
        <div className="percentContainer">
          {(isLoading) ? <span className="percentText">Loading...</span> : <span className="percentText">{percent.toFixed(0)}% Positivity</span>}
          <div className="filledPercentContainer">
            <div className="filledPercent" style={{width: `${percent}%`, backgroundColor: fillColor}}></div>
          </div>
        </div>
      </div>
      <div className="credits">Made by <span>Ravi Maurya</span></div>
    </div>
  );
}

export default Home;