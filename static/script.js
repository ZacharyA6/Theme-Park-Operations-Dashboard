// Retrieve current ride data from the flask API and build the dashboard
async function loadRides() {
    try {

        const response = await fetch("/api/rides");

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const rides = await response.json();

        const container =
            document.getElementById("rides-container");

        // clear existing cards before rebuilding them with current values
        container.innerHTML = "";

        rides.forEach(ride => {

            const card =
                document.createElement("div");

            // Add the ride status as a CSS class so the card color reflects its status
            card.className = `ride-card ${ride.status.toLowerCase()}`;

            card.innerHTML = `
                <h2>${ride.name}</h2>

                <p>${ride.ride_type}</p>

                <label>Status</label>

                <select id="status-${ride.id}">
                    <option
                        ${ride.status === "Operating"
                            ? "selected" : ""}
                        >
                            Operating
                        </option>

                    <option
                        ${ride.status === "Delayed"
                            ? "selected" : ""}
                        >
                            Delayed
                        </option>

                    <option
                        ${ride.status === "Closed"
                            ? "selected" : ""}
                        >
                            Closed
                        </option>
                    </select>

                    <label>Wait Time</label>

                    <input
                        id="wait-${ride.id}"
                        type = "number"
                        min = "0"
                        max = "240"
                        value="${ride.wait_time}"
                    >

                    <label>Capacity</label>

                    <input
                        id="capacity-${ride.id}"
                        type = "number"
                        min = "1"
                        max = "100"
                        value="${ride.capacity}"
                    >

                    <button onclick="updateRide(${ride.id}, '${ride.name}')">
                        Update Ride
                    </button>
            `;

            container.appendChild(card);
        });
    } catch(error) {
        console.error(error);

        alert("Could not connect to the server. Please try again.")
    }
}

async function updateRide(id, rideName) {
    try {
        
        const status =
            document.getElementById(
                `status-${id}`
            ).value;

        const waitTime =
            document.getElementById(
                `wait-${id}`
            ).value;

        const capacity =
            document.getElementById(
                `capacity-${id}`
            ).value;

        //check for empty wait time and capacity
        if (waitTime === "" && capacity === "") {
            alert("Wait time and capacity fields must have values.");
            return;
        }

        //validate wait time
        if (waitTime === "" || waitTime < 0 || waitTime > 240) {
            alert("Wait time must be between 0 and 240.");
            return;
        }

        //validate capacity
        if (capacity === "" || capacity < 1 || capacity > 100) {
            alert("Capacity must be between 1 and 100.");
            return;
        }

        //Send the updated ride information to the flask PUT endpoint
        const response = await fetch(`/api/rides/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                status: status,
                wait_time: Number(waitTime),
                capacity: Number(capacity)
            })
        });

        //HTTP errors do not cause fetch() to throw,
        //so convert unsuccessful responses into an error
        if (!response.ok) {
            const errorData = await response.json;

            alert(errorData.error || "Failed to update ride.");

            return;
        }

        showToast(`${rideName} updated successfully.`);

        loadRides();
    } catch(error) {
        console.error(error);

        alert("Could not update the ride. Please try again.");
    }
    
}

//Show a temporary success notification
function showToast(message) {
    const toast = document.getElementById("toast");

    toast.textContent = message;

    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 3000);
}

loadRides();