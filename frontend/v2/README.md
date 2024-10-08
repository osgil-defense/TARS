# TARS Frontend

⚠️ This new frontend code for TARS is still in alpha, with serious bugs and a lack of features.

## About

The new frontend for TARS. This code was originally hosted at the [TARS-frontend](https://github.com/osgil-defense/TARS-frontend) repo but has sense been moved to the main [TARS](https://github.com/osgil-defense/TARS) repo.

## How To Start

1. Install [Node.js](https://nodejs.org/en)
2. Create a ".env" file. Refer to the ".template_env" file see what you need to provide in the ".env" file for.
3. Install dependencies:
   ```bash
   npm install
   ```
4. Start the web app:
   ```bash
   npm start
   ```
5. In your browser, go to: http://localhost:3000/

## Notes

- React's official React Browser Extension for debugging: https://react.dev/learn/react-developer-tools

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run format`

Format the code layout to keep everything clean. Make sure to install prettier (`npx prettier --write "src/**/*.{js,jsx,css,scss}"`) before running this script.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.
