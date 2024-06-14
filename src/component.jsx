
import './App.css';
import org from "./assets/original.jpg"
import det from "./assets/detected.jpg"
import no_img from "./assets/no_img.jpg"

import React, { useState } from 'react'
import axios from 'axios'



function Component1() {

  const[image, setImage] = useState(no_img)
  const[query, setQuery] = useState('')
  const[detected, setDetected] = useState()
  const[display, setDisplay] = useState()
  // const[url, setUrl] = useState('')




  const changed = async(e)=>
    {
        
        try {
          const formData = new FormData();
          formData.append('image', e.target.files[0]);
    
          const response = await axios.post('/upload', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });
          
          console.log('Image uploaded successfully:', response.data);
        } catch (error) {
          console.error('Error uploading image:', error);
        }
    }
  const handleQuery = (e) => 
    {
      setDisplay(true)
      setDetected(true)
      setQuery(e.target.value)
      setImage(no_img)

    };

  const handleSubmit = async(e) =>
    {
      
      try {
        const formData1 = new FormData();
        formData1.append('query', query);
  
        const response = await axios.post('/generate', formData1, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        // console.log('FormData:', formData1.get('query'));
        console.log('Query uploaded Successfully', response.data);
        setDisplay(false)
        setDetected(response.data.detected)
        setImage(response.data.image);
        
        // console.log(object)
      } catch (error) {
        console.error('Error uploading query:', error);
      }
      
    }
    

  return (
    <div className="App">
      <h1>Object Detection</h1>
      <div className="box">
        {/* <img src={org} alt="" /> */}
        
        <div className="left">
          <div style={{backgroundImage: `url(${org})`}}  className="original"></div>
          <input type="file" onChange={changed} id = "upload"/>
          
          <input placeholder='Enter Objects' className='text' type="text" value={query} onChange={handleQuery}/>
          <div className="buttons">
          <label htmlFor="upload">SELECT IMAGE</label>
          <button onClick={handleSubmit}>SUBMIT</button>
          </div>
        </div>
        <div className="right">
        {detected? <img className = "detected" src={display? image : `data:image/jpeg;base64,${image}`}/> : <p>NO OBJECTS DETECTED</p>}
        </div>
      </div>
    </div>
  )
}

export default Component1
