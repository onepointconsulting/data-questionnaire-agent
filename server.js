import express, { Router } from "express";
import cors from 'cors';

const app = express();
const port = 8000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cors());

const users = [
    {
        '_id': 1,
        'name': 'Ritwik Math'
    },{
        '_id': 2,
        'name': 'John Doe'
    },{
        '_id': 3,
        'name': 'Jane Doe'
    }
]

const promise = new Promise((resolve, reject) => {
    setTimeout(() => {
        resolve(users)
    }, 3000)
})

const route = Router();

route.get('/users', async (req, res, next) => {
    try {
        const data = await promise;
        return res.status(200).json({
            'message': 'Fetched successfully',
            'users': data
        })
    } catch (error) {
        console.log(error.message)
    }
});

app.use(route);

app.listen(port, () => {
    console.log(`App is running on http://localhost:${port}`)
})
