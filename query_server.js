const { GameDig } = require('gamedig');

const args = process.argv.slice(2);
const game = args[0];
const address = args[1];
const port = args[2];

console.log(`Querying game server: ${game} ${address} ${port}`);

async function queryServer(game, address, port) {
    try {
        const response = await GameDig.query({
            type: game,
            host: address,
            port: port
        });
        return response;
    } catch (error) {
        console.error('Error querying game server:', error);
        return null;
    }
}

queryServer(game, address, port).then(console.log);
