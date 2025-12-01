// Stations
const stations = [
  { name: "Vytilla", lat: 9.9787, lng: 76.2979 },
  { name: "High Court", lat: 9.9822, lng: 76.2765 },
  { name: "Vypin", lat: 10.004, lng: 76.233 },
  { name: "Kakkanad", lat: 10.0197, lng: 76.3572 },
  { name: "South Chittoor", lat: 10.0346, lng: 76.2907 },
  { name: "Cheranalloor", lat: 10.027, lng: 76.292 },
  { name: "Eloor", lat: 10.0525, lng: 76.3102 },
  { name: "Fort Kochi", lat: 9.9659, lng: 76.2426 }
];

// Graph edges
const edges = [
  ["Vytilla","High Court"],
  ["High Court","Vypin"],
  ["High Court","Fort Kochi"],
  ["Cheranalloor","South Chittoor"],
  ["South Chittoor","Eloor"]
];

// Build adjacency
const adj = {};
stations.forEach(s => adj[s.name] = []);
edges.forEach(([a,b]) => { adj[a].push(b); adj[b].push(a); });

// BFS shortest route
function getRoute(src, dst){
  let q = [[src]];
  let visited = new Set([src]);

  while(q.length){
    let path = q.shift();
    let last = path[path.length-1];

    if(last === dst) return path;

    adj[last].forEach(n=>{
      if(!visited.has(n)){
        visited.add(n);
        q.push([...path, n]);
      }
    });
  }
  return null;
}

// Populate dropdowns
stations.forEach(s => {
  source.append(new Option(s.name, s.name));
  destination.append(new Option(s.name, s.name));
});

// Initialize map
const map = L.map("map").setView([9.985, 76.28], 12.8);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);

stations.forEach(st => L.marker([st.lat, st.lng]).addTo(map).bindPopup(st.name));

let routeLayer = null;
let arrowMarker = null;

// Form submission
document.getElementById("journeyForm").onsubmit = function(e){
  e.preventDefault();

  let src = source.value;
  let dst = destination.value;

  if(!src || !dst || src === dst) return;

  let route = getRoute(src,dst);
  if(!route){ alert("No route found."); return; }

  // Remove previous route
  if(routeLayer) map.removeLayer(routeLayer);
  if(arrowMarker) map.removeLayer(arrowMarker);

  const points = route.map(st=>{
    const s = stations.find(x=>x.name===st);
    return [s.lat,s.lng];
  });

  routeLayer = L.polyline(points, {color:"blue",weight:5}).addTo(map);

  // Arrow
  const from = points.at(-2);
  const to = points.at(-1);
  const angle = Math.atan2(to[1]-from[1], to[0]-from[0]) * 180/Math.PI;

  arrowMarker = L.marker(to, {
    icon: L.divIcon({
      html:`<svg width="30" height="30" style="transform:rotate(${90-angle}deg);"><polygon points="15,0 30,30 15,22 0,30" fill="#134ae3"/></svg>`
    }),
    interactive:false
  }).addTo(map);

  map.fitBounds(routeLayer.getBounds(), {padding:[40,40]});

  // Show route list
  routeList.innerHTML = "";
  route.forEach(x=> routeList.innerHTML += `<li>${x}</li>`);

  fareDisplay.textContent = `Fare: ₹${20 + 10*(route.length-1)}`;
  result.style.display = "block";
};
