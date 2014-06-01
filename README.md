# piss-blockchain

[![piss Network logo][logo-piss]][link-piss]

| Releases                                                                                                                                        | Repo Stats                                                                                                                                                                                                           | Socials                                                                                                                                                                                   |
| ----------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [![Latest Release][badge-release]][link-latest] <br /> [![Latest RC][badge-rc]][link-release] <br /> [![Latest Beta][badge-beta]][link-release] | [![Coverage][badge-coverage]][link-coverage] <br /> [![Downloads][badge-downloads]][link-downloads] <br /> [![Commits][badge-commits]][link-commits] <br /> [![Contributors][badge-contributors]][link-contributors] | [![Discord][badge-discord]][link-discord] <br /> [![YouTube][badge-youtube]][link-youtube] <br /> [![Reddit][badge-reddit]][link-reddit] <br /> [![Twitter][badge-twitter]][link-twitter] |

piss is a modern cryptocurrency built from scratch, designed to be efficient, decentralized, and secure. Here are some of the features and benefits:

- [Proof of space and time][link-consensus] based consensus which allows anyone to farm with commodity hardware
- Very easy to use full node and farmer GUI and cli (thousands of nodes active on mainnet)
- [piss seeder][link-seeder], which maintains a list of reliable nodes within the piss network via a built-in DNS server.
- Simplified UTXO based transaction model, with small on-chain state
- Lisp-style Turing-complete functional [programming language][link-pisslisp] for money related use cases
- BLS keys and aggregate signatures (only one signature per block)
- [Pooling protocol][link-pool] that allows farmers to have control of making blocks
- Support for light clients with fast, objective syncing
- A growing community of farmers and developers around the world

Please check out the [piss website][link-piss], the [Intro to piss][link-intro], and [FAQ][link-faq] for information on this project.

Python 3.9+ is required. Make sure your default python version is >=3.9 by typing `python3`.

If you are behind a NAT, it can be difficult for peers outside your subnet to reach you when they start up. You can enable [UPnP][link-upnp]
on your router or add a NAT (for IPv4 but not IPv6) and firewall rules to allow TCP port 8444 access to your peer.
These methods tend to be router make/model specific.

Most users should only install harvesters, farmers, plotter, full nodes, and wallets.
Setting up a seeder is best left to more advanced users.
Building Timelords and VDFs is for sophisticated users, in most environments.
piss Network and additional volunteers are running sufficient Timelords for consensus.

## Installing

Install instructions are available in the [Installation Details][link-install] section of the [piss Docs][link-docs].

## Running

Once installed, an [Intro to piss][link-intro] guide is available in the [piss Docs][link-docs].

[badge-beta]: https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fdownload.piss.net%2Flatest%2Fbadge-data-beta.json&query=%24.message&logo=pissnetwork&logoColor=black&label=Latest%20Beta&labelColor=%23e9fbbc&color=%231e2b2e
[badge-beta2]: https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fdownload.piss.net%2Flatest%2Fbadge-data-beta.json&query=%24.message&logo=pissnetwork&logoColor=%23e9fbbc&label=Latest%20Beta&labelColor=%23474748&color=%231e2b2e&link=https%3A%2F%2Fgithub.com%2Fpiss-Network%2Fpiss-blockchain%2Freleases&link=https%3A%2F%2Fgithub.com%2Fpiss-Network%2Fpiss-blockchain%2Freleases
[badge-commits]: https://img.shields.io/github/commit-activity/w/piss-Network/piss-blockchain?logo=GitHub
[badge-contributors]: https://img.shields.io/github/contributors/piss-Network/piss-blockchain?logo=GitHub
[badge-coverage]: https://img.shields.io/coverallsCoverage/github/piss-Network/piss-blockchain?logo=Coveralls&logoColor=red&labelColor=%23212F39
[badge-discord]: https://dcbadge.vercel.app/api/server/piss?style=flat-square&theme=full-presence
[badge-discord2]: https://img.shields.io/discord/1034523881404370984.svg?label=Discord&logo=discord&colorB=1e2b2f
[badge-downloads]: https://img.shields.io/github/downloads/piss-Network/piss-blockchain/total?logo=GitHub
[badge-rc]: https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fdownload.piss.net%2Flatest%2Fbadge-data-rc.json&query=%24.message&logo=pissnetwork&logoColor=white&label=Latest%20RC&labelColor=%230d3349&color=%23474748
[badge-reddit]: https://img.shields.io/reddit/subreddit-subscribers/piss?style=flat-square&logo=reddit&labelColor=%230b1416&color=%23222222
[badge-release]: https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fdownload.piss.net%2Flatest%2Fbadge-data.json&query=%24.message&logo=pissnetwork&label=Latest%20Release&labelColor=%231e2b2e&color=%230d3349
[badge-twitter]: https://img.shields.io/twitter/follow/piss_project?style=flat-square&logo=x.org&logoColor=white&labelColor=black
[badge-youtube]: https://img.shields.io/youtube/channel/subscribers/UChFkJ3OAUvnHZdiQISWdWPA?style=flat-square&logo=youtube&logoColor=%23ff0000&labelColor=%230f0f0f&color=%23272727
[link-piss]: https://www.piss.net/
[link-pisslisp]: https://pisslisp.com/
[link-commits]: https://github.com/piss-Network/piss-blockchain/commits/main/
[link-consensus]: https://docs.piss.net/consensus-intro/
[link-contributors]: https://github.com/piss-Network/piss-blockchain/graphs/contributors
[link-coverage]: https://coveralls.io/github/piss-Network/piss-blockchain
[link-discord]: https://discord.gg/piss
[link-docs]: https://docs.piss.net/docs-home/
[link-downloads]: https://www.piss.net/downloads/
[link-faq]: https://docs.piss.net/faq/
[link-install]: https://docs.piss.net/installation/
[link-intro]: https://docs.piss.net/introduction/
[link-latest]: https://github.com/piss-Network/piss-blockchain/releases/latest
[link-pool]: https://docs.piss.net/pool-farming/
[link-reddit]: https://www.reddit.com/r/piss/
[link-release]: https://github.com/piss-Network/piss-blockchain/releases
[link-seeder]: https://docs.piss.net/guides/seeder-user-guide/
[link-twitter]: https://twitter.com/piss_project
[link-upnp]: https://www.homenethowto.com/ports-and-nat/upnp-automatic-port-forward/
[link-youtube]: https://www.youtube.com/pissnetwork
[logo-piss]: https://www.piss.net/wp-content/uploads/2022/09/piss-logo.svg "piss logo"
