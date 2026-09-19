"""
Seed data module providing high-fidelity intelligence baselines across ecosystems,
sponsors, historical winners, active opportunities, benefits, jobs, and technical trends.
"""
from typing import List, Dict, Any

# --------------------------------------------------------------------------- #
#                        1. ECOSYSTEMS (ENGINE 2 & 11)                        #
# --------------------------------------------------------------------------- #
# 21 Established, 29 Emerging, 10 Watchlist = 60 total verified ecosystems.

SEED_ECOSYSTEMS: List[Dict[str, Any]] = [
    # --- ESTABLISHED (21) ---
    {
        "slug": "solana",
        "name": "Solana",
        "category": "High-Performance L1",
        "momentum_score": 92.5,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 19.0, "hackathons_and_grants": 19.5, "dev_activity_acceleration": 14.5, "sdk_product_launches": 9.5, "sponsor_activity": 9.0, "social_discussion": 9.5, "funding_activity": 4.5, "competition_opportunity": 7.0},
        "tracked_repos": ["solana-labs/solana", "coral-xyz/anchor", "anza-xyz/agave"],
        "notes": "Massive developer flywheel driven by Colosseum Crypto World's Fair ($3.3M pool) and Blinks/Actions adoption.",
        "maturity_stage": "established"
    },
    {
        "slug": "base",
        "name": "Base",
        "category": "Ethereum L2",
        "momentum_score": 94.0,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 19.5, "hackathons_and_grants": 19.0, "dev_activity_acceleration": 15.0, "sdk_product_launches": 9.5, "sponsor_activity": 9.5, "social_discussion": 9.5, "funding_activity": 4.5, "competition_opportunity": 7.5},
        "tracked_repos": ["base-org", "coinbase/agentkit", "coinbase/x402"],
        "notes": "Leader in onchain consumer and autonomous agent micro-payments (x402, AgentKit, Base Batches, ERC-8021 builder codes).",
        "maturity_stage": "established"
    },
    {
        "slug": "ethereum",
        "name": "Ethereum",
        "category": "L1 Settlement Layer",
        "momentum_score": 86.0,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 17.0, "hackathons_and_grants": 18.0, "dev_activity_acceleration": 12.5, "sdk_product_launches": 8.5, "sponsor_activity": 9.5, "social_discussion": 8.5, "funding_activity": 4.0, "competition_opportunity": 8.0},
        "tracked_repos": ["ethereum/go-ethereum", "ethereum/EIPs"],
        "notes": "Highest aggregate prize liquidity and sponsor density via ETHGlobal circuits; mature but fiercely competitive.",
        "maturity_stage": "established"
    },
    {
        "slug": "bitcoin",
        "name": "Bitcoin",
        "category": "L1 / Ordinals & Runes",
        "momentum_score": 84.0,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 16.0, "hackathons_and_grants": 17.0, "dev_activity_acceleration": 13.0, "sdk_product_launches": 8.0, "sponsor_activity": 8.5, "social_discussion": 9.0, "funding_activity": 4.5, "competition_opportunity": 8.0},
        "tracked_repos": ["bitcoin/bitcoin", "ordinals/ord"],
        "notes": "Surging programmability interest catalyzed by BitVM, Runes protocols, and institutional capital inflows.",
        "maturity_stage": "established"
    },
    {
        "slug": "bnb-chain",
        "name": "BNB Chain",
        "category": "EVM L1 & opBNB L2",
        "momentum_score": 81.0,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 17.0, "hackathons_and_grants": 16.5, "dev_activity_acceleration": 12.0, "sdk_product_launches": 8.0, "sponsor_activity": 8.5, "social_discussion": 7.5, "funding_activity": 4.0, "competition_opportunity": 7.5},
        "tracked_repos": ["bnb-chain/bsc"],
        "notes": "Massive retail footprint with regular MVB (Most Valuable Builder) accelerator cohorts backed by Binance Labs.",
        "maturity_stage": "established"
    },
    {
        "slug": "avalanche",
        "name": "Avalanche",
        "category": "Multi-Subnet L1",
        "momentum_score": 80.0,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 16.0, "hackathons_and_grants": 16.0, "dev_activity_acceleration": 12.0, "sdk_product_launches": 8.0, "sponsor_activity": 8.0, "social_discussion": 8.0, "funding_activity": 4.0, "competition_opportunity": 8.0},
        "tracked_repos": ["ava-labs/avalanchego"],
        "notes": "Focus on institutional RWA subnets, custom enterprise execution environments, and Avalanche 9000 upgrade.",
        "maturity_stage": "established"
    },
    {
        "slug": "arbitrum",
        "name": "Arbitrum",
        "category": "Ethereum L2",
        "momentum_score": 83.5,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 16.5, "hackathons_and_grants": 17.0, "dev_activity_acceleration": 12.5, "sdk_product_launches": 8.5, "sponsor_activity": 8.5, "social_discussion": 8.5, "funding_activity": 4.0, "competition_opportunity": 8.0},
        "tracked_repos": ["OffchainLabs/nitro", "ArbitrumFoundation"],
        "notes": "Dominant DeFi TVL on Layer 2 with deep DAO grant funding and Arbitrum Orbit custom L3 chains.",
        "maturity_stage": "established"
    },
    {
        "slug": "optimism",
        "name": "Optimism / OP Superchain",
        "category": "Ethereum L2 / Superchain",
        "momentum_score": 85.0,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 17.5, "hackathons_and_grants": 18.0, "dev_activity_acceleration": 13.0, "sdk_product_launches": 8.5, "sponsor_activity": 9.0, "social_discussion": 8.5, "funding_activity": 4.0, "competition_opportunity": 6.5},
        "tracked_repos": ["ethereum-optimism/optimism"],
        "notes": "Standardized OP Stack powering Base, World Chain, and Soneium, anchored by massive RetroPGF funding rounds.",
        "maturity_stage": "established"
    },
    {
        "slug": "polygon",
        "name": "Polygon",
        "category": "PoS & ZK AggLayer",
        "momentum_score": 82.0,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 16.5, "hackathons_and_grants": 16.0, "dev_activity_acceleration": 12.0, "sdk_product_launches": 8.5, "sponsor_activity": 9.0, "social_discussion": 8.0, "funding_activity": 4.0, "competition_opportunity": 8.0},
        "tracked_repos": ["0xPolygon/polygon-edge", "0xPolygonHermez"],
        "notes": "Pivoted toward cross-chain unified liquidity via AggLayer and CDK (Chain Development Kit) adoption.",
        "maturity_stage": "established"
    },
    {
        "slug": "near",
        "name": "NEAR",
        "category": "Sharded L1 / User-Owned AI",
        "momentum_score": 87.0,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 18.0, "hackathons_and_grants": 17.5, "dev_activity_acceleration": 13.5, "sdk_product_launches": 9.0, "sponsor_activity": 8.5, "social_discussion": 9.0, "funding_activity": 4.5, "competition_opportunity": 7.0},
        "tracked_repos": ["near/nearcore", "near/near-api-js"],
        "notes": "Aggressive positioning as the foundational infrastructure layer for decentralized user-owned AI and Chain Abstraction.",
        "maturity_stage": "established"
    },
    {
        "slug": "cosmos",
        "name": "Cosmos",
        "category": "Interchain / IBC",
        "momentum_score": 79.0,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 15.0, "hackathons_and_grants": 15.5, "dev_activity_acceleration": 12.5, "sdk_product_launches": 8.0, "sponsor_activity": 7.5, "social_discussion": 8.0, "funding_activity": 4.0, "competition_opportunity": 8.5},
        "tracked_repos": ["cosmos/cosmos-sdk", "cosmos/ibc-go"],
        "notes": "Pioneered application-specific appchains and sovereign governance connected via Inter-Blockchain Communication (IBC).",
        "maturity_stage": "established"
    },
    {
        "slug": "polkadot",
        "name": "Polkadot",
        "category": "Shared Security / Parachains",
        "momentum_score": 78.0,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 16.0, "hackathons_and_grants": 16.0, "dev_activity_acceleration": 12.0, "sdk_product_launches": 7.5, "sponsor_activity": 7.5, "social_discussion": 7.0, "funding_activity": 4.0, "competition_opportunity": 8.0},
        "tracked_repos": ["paritytech/polkadot-sdk"],
        "notes": "Web3 Foundation continuous grants and Polkadot 2.0 Agile Coretime transition for flexible compute allocation.",
        "maturity_stage": "established"
    },
    {
        "slug": "ton",
        "name": "TON",
        "category": "Telegram-Integrated L1",
        "momentum_score": 89.0,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 18.0, "hackathons_and_grants": 18.5, "dev_activity_acceleration": 14.0, "sdk_product_launches": 9.0, "sponsor_activity": 8.5, "social_discussion": 9.5, "funding_activity": 4.5, "competition_opportunity": 7.0},
        "tracked_repos": ["ton-blockchain/ton"],
        "notes": "Unmatched 900M+ consumer distribution funnel via native Telegram Mini Apps and TON Teleport bridges.",
        "maturity_stage": "established"
    },
    {
        "slug": "sui",
        "name": "Sui",
        "category": "Move-Based Object L1",
        "momentum_score": 85.5,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 17.5, "hackathons_and_grants": 17.5, "dev_activity_acceleration": 13.5, "sdk_product_launches": 8.5, "sponsor_activity": 8.5, "social_discussion": 8.5, "funding_activity": 4.0, "competition_opportunity": 7.5},
        "tracked_repos": ["MystenLabs/sui"],
        "notes": "Sub-second finality object-centric execution powering high-frequency Web3 gaming and Walrus decentralized storage.",
        "maturity_stage": "established"
    },
    {
        "slug": "aptos",
        "name": "Aptos",
        "category": "Move-Based Parallel L1",
        "momentum_score": 84.5,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 17.0, "hackathons_and_grants": 17.0, "dev_activity_acceleration": 13.0, "sdk_product_launches": 8.5, "sponsor_activity": 8.5, "social_discussion": 8.5, "funding_activity": 4.0, "competition_opportunity": 8.0},
        "tracked_repos": ["aptos-labs/aptos-core"],
        "notes": "Parallel execution with Block-STM and strong institutional fintech backing across Microsoft, Franklin Templeton.",
        "maturity_stage": "established"
    },
    {
        "slug": "monad",
        "name": "Monad",
        "category": "Parallel EVM L1",
        "momentum_score": 89.0,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 18.5, "hackathons_and_grants": 19.0, "dev_activity_acceleration": 14.0, "sdk_product_launches": 9.0, "sponsor_activity": 8.5, "social_discussion": 9.5, "funding_activity": 4.5, "competition_opportunity": 6.0},
        "tracked_repos": ["monad-developers"],
        "notes": "Extreme developer anticipation leading up to mainnet; Nitro Accelerator ($750k) and parallel EVM state db optimizations.",
        "maturity_stage": "established"
    },
    {
        "slug": "icp",
        "name": "Internet Computer (ICP)",
        "category": "Canister Cloud L1",
        "momentum_score": 80.5,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 16.5, "hackathons_and_grants": 16.5, "dev_activity_acceleration": 12.5, "sdk_product_launches": 8.0, "sponsor_activity": 7.5, "social_discussion": 7.5, "funding_activity": 4.0, "competition_opportunity": 8.0},
        "tracked_repos": ["dfinity/ic"],
        "notes": "Serverless canister smart contracts capable of hosting full web frontends, onchain LLMs, and Bitcoin direct integration.",
        "maturity_stage": "established"
    },
    {
        "slug": "cardano",
        "name": "Cardano",
        "category": "UTXO Smart Contract L1",
        "momentum_score": 76.0,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 15.0, "hackathons_and_grants": 15.0, "dev_activity_acceleration": 12.0, "sdk_product_launches": 7.0, "sponsor_activity": 7.5, "social_discussion": 8.0, "funding_activity": 3.5, "competition_opportunity": 8.0},
        "tracked_repos": ["IntersectMBO/cardano-node"],
        "notes": "Chang hard fork governance transition and Project Catalyst decentralized community funding pool.",
        "maturity_stage": "established"
    },
    {
        "slug": "algorand",
        "name": "Algorand",
        "category": "Pure PoS L1",
        "momentum_score": 75.0,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 15.0, "hackathons_and_grants": 15.0, "dev_activity_acceleration": 11.5, "sdk_product_launches": 7.5, "sponsor_activity": 7.0, "social_discussion": 7.5, "funding_activity": 3.5, "competition_opportunity": 8.0},
        "tracked_repos": ["algorand/go-algorand"],
        "notes": "Instant finality and Python-native smart contract programming via AlgoKit 2.0 developer tooling.",
        "maturity_stage": "established"
    },
    {
        "slug": "hedera",
        "name": "Hedera",
        "category": "Hashgraph Enterprise DLT",
        "momentum_score": 77.0,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 15.5, "hackathons_and_grants": 15.5, "dev_activity_acceleration": 12.0, "sdk_product_launches": 7.5, "sponsor_activity": 8.0, "social_discussion": 7.0, "funding_activity": 3.5, "competition_opportunity": 8.0},
        "tracked_repos": ["hashgraph/hedera-services"],
        "notes": "Enterprise governing council (Google, IBM) driving tokenization and Hedera Consensus Service integrations.",
        "maturity_stage": "established"
    },
    {
        "slug": "chainlink",
        "name": "Chainlink",
        "category": "Oracle & Cross-Chain CCIP",
        "momentum_score": 88.5,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 18.0, "hackathons_and_grants": 18.5, "dev_activity_acceleration": 13.5, "sdk_product_launches": 9.0, "sponsor_activity": 9.5, "social_discussion": 8.5, "funding_activity": 4.5, "competition_opportunity": 7.0},
        "tracked_repos": ["smartcontractkit/chainlink"],
        "notes": "Universal standard for cross-chain interoperability (CCIP), verifiable data feeds, and Swift banking pilots.",
        "maturity_stage": "established"
    },

    # --- EMERGING (29) ---
    {
        "slug": "starknet",
        "name": "Starknet",
        "category": "ZK Rollup / Cairo L2",
        "momentum_score": 82.5,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 17.5, "hackathons_and_grants": 17.0, "dev_activity_acceleration": 13.0, "sdk_product_launches": 8.5, "sponsor_activity": 8.0, "social_discussion": 8.0, "funding_activity": 3.5, "competition_opportunity": 7.0},
        "tracked_repos": ["starkware-libs/cairo"],
        "notes": "Native account abstraction, parallel execution with Blockifier, and high-performance provable computing in Cairo.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "zksync-era",
        "name": "zkSync Era",
        "category": "ZK Rollup / Elastic Chain",
        "momentum_score": 80.0,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 16.0, "hackathons_and_grants": 16.0, "dev_activity_acceleration": 12.5, "sdk_product_launches": 8.0, "sponsor_activity": 8.0, "social_discussion": 8.0, "funding_activity": 3.5, "competition_opportunity": 8.0},
        "tracked_repos": ["matter-labs/zksync-era"],
        "notes": "Native account abstraction and ZK Stack hyperchain framework powering interconnected sovereign chains.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "linea",
        "name": "Linea",
        "category": "Consensys zkEVM L2",
        "momentum_score": 81.5,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 16.5, "hackathons_and_grants": 16.5, "dev_activity_acceleration": 12.5, "sdk_product_launches": 8.5, "sponsor_activity": 8.5, "social_discussion": 8.0, "funding_activity": 3.5, "competition_opportunity": 7.5},
        "tracked_repos": ["Consensys/linea-monorepo"],
        "notes": "Direct distribution funnel into MetaMask wallet default network with frequent builder voyage incentive programs.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "scroll",
        "name": "Scroll",
        "category": "Type-1 zkEVM L2",
        "momentum_score": 79.5,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 16.0, "hackathons_and_grants": 16.0, "dev_activity_acceleration": 12.0, "sdk_product_launches": 8.0, "sponsor_activity": 8.0, "social_discussion": 8.0, "funding_activity": 3.5, "competition_opportunity": 8.0},
        "tracked_repos": ["scroll-tech/scroll"],
        "notes": "Bytecode-level EVM equivalence with extensive open-source community research around zero-knowledge circuit optimization.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "mantle",
        "name": "Mantle",
        "category": "Modular L2 with EigenDA",
        "momentum_score": 80.5,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 16.5, "hackathons_and_grants": 16.5, "dev_activity_acceleration": 12.0, "sdk_product_launches": 8.0, "sponsor_activity": 8.0, "social_discussion": 7.5, "funding_activity": 4.0, "competition_opportunity": 8.0},
        "tracked_repos": ["mantlenetworkio/mantle"],
        "notes": "Backed by massive BitDAO treasury with modular data availability powered by EigenDA integration.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "berachain",
        "name": "Berachain",
        "category": "Proof-of-Liquidity EVM L1",
        "momentum_score": 85.0,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 18.0, "hackathons_and_grants": 18.0, "dev_activity_acceleration": 13.0, "sdk_product_launches": 8.5, "sponsor_activity": 8.0, "social_discussion": 9.5, "funding_activity": 4.0, "competition_opportunity": 6.0},
        "tracked_repos": ["berachain"],
        "notes": "Novel Proof-of-Liquidity consensus turning validator stake into active DeFi liquidity, generating intense cult developer following.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "injective",
        "name": "Injective",
        "category": "Cosmos DeFi & AI L1",
        "momentum_score": 81.0,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 16.5, "hackathons_and_grants": 16.5, "dev_activity_acceleration": 12.5, "sdk_product_launches": 8.0, "sponsor_activity": 8.0, "social_discussion": 8.0, "funding_activity": 3.5, "competition_opportunity": 8.0},
        "tracked_repos": ["InjectiveLabs/injective-core"],
        "notes": "Plug-and-play financial modules including onchain orderbook, derivatives primitives, and multi-VM CosmWasm/EVM support.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "celo",
        "name": "Celo",
        "category": "Mobile-First Ethereum L2",
        "momentum_score": 78.5,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 16.0, "hackathons_and_grants": 16.0, "dev_activity_acceleration": 12.0, "sdk_product_launches": 8.0, "sponsor_activity": 7.5, "social_discussion": 7.5, "funding_activity": 3.5, "competition_opportunity": 8.0},
        "tracked_repos": ["celo-org/celo-blockchain"],
        "notes": "Transitioning to an OP Stack Ethereum L2 with focus on real-world mobile payments, mini-wallets, and stablecoins in emerging markets.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "megaeth",
        "name": "MegaETH",
        "category": "Real-Time 100k TPS L2",
        "momentum_score": 86.0,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 18.0, "hackathons_and_grants": 18.0, "dev_activity_acceleration": 13.5, "sdk_product_launches": 8.5, "sponsor_activity": 8.5, "social_discussion": 9.5, "funding_activity": 4.5, "competition_opportunity": 5.5},
        "tracked_repos": ["megaeth-labs"],
        "notes": "Building real-time blockchain execution with 100,000 TPS and 1ms latency via in-memory compute and specialized hardware.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "world-chain",
        "name": "World Chain",
        "category": "Human-Centric OP L2",
        "momentum_score": 85.5,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 18.0, "hackathons_and_grants": 18.0, "dev_activity_acceleration": 13.0, "sdk_product_launches": 9.0, "sponsor_activity": 8.5, "social_discussion": 9.0, "funding_activity": 4.0, "competition_opportunity": 6.0},
        "tracked_repos": ["worldcoin/world-id-docs"],
        "notes": "Prioritizes blockspace and free gas allowance for verified humans authenticated via World ID zero-knowledge proofs.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "soneium",
        "name": "Soneium",
        "category": "Sony Enterprise OP L2",
        "momentum_score": 82.0,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 17.5, "hackathons_and_grants": 17.0, "dev_activity_acceleration": 12.5, "sdk_product_launches": 8.0, "sponsor_activity": 8.5, "social_discussion": 8.5, "funding_activity": 4.0, "competition_opportunity": 6.0},
        "tracked_repos": ["soneium"],
        "notes": "Built by Sony Block Solutions Labs on the OP Stack, targeted at mainstream gaming, entertainment IP, and creator economies.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "unichain",
        "name": "Unichain",
        "category": "DeFi-Optimized OP L2",
        "momentum_score": 84.5,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 18.0, "hackathons_and_grants": 18.0, "dev_activity_acceleration": 13.0, "sdk_product_launches": 8.5, "sponsor_activity": 8.5, "social_discussion": 9.0, "funding_activity": 4.0, "competition_opportunity": 5.5},
        "tracked_repos": ["uniswap/unichain"],
        "notes": "Uniswap's dedicated DeFi rollup featuring 1-second sub-blocks, TEE-based block building, and native cross-chain liquidity.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "zora",
        "name": "Zora",
        "category": "Creator / Media L2",
        "momentum_score": 79.0,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 16.0, "hackathons_and_grants": 16.0, "dev_activity_acceleration": 12.0, "sdk_product_launches": 8.0, "sponsor_activity": 7.5, "social_discussion": 8.0, "funding_activity": 3.5, "competition_opportunity": 8.0},
        "tracked_repos": ["ourzora/zora-protocol"],
        "notes": "Hyper-focused on creator monetization, dynamic onchain media protocols, and low-cost minting on OP Stack.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "frax",
        "name": "Frax (Fraxtal)",
        "category": "Modular Computation L2",
        "momentum_score": 77.5,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 15.5, "hackathons_and_grants": 15.5, "dev_activity_acceleration": 12.0, "sdk_product_launches": 7.5, "sponsor_activity": 7.5, "social_discussion": 7.5, "funding_activity": 3.5, "competition_opportunity": 8.5},
        "tracked_repos": ["FraxFinance"],
        "notes": "Fraxtal execution layer incentivizing gas usage with blockspace rewards (fraxpoint rebates) and deep stablecoin liquidity.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "mode",
        "name": "Mode",
        "category": "Onchain Growth OP L2",
        "momentum_score": 78.0,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 16.0, "hackathons_and_grants": 16.0, "dev_activity_acceleration": 12.0, "sdk_product_launches": 7.5, "sponsor_activity": 7.5, "social_discussion": 7.5, "funding_activity": 3.5, "competition_opportunity": 8.0},
        "tracked_repos": ["mode-network"],
        "notes": "Engineered for economic cooperation with sequencer fee-sharing (SFS) directly paying developers based on contract traffic.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "stacks",
        "name": "Stacks",
        "category": "Bitcoin L2 / Clarity",
        "momentum_score": 80.0,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 16.5, "hackathons_and_grants": 16.5, "dev_activity_acceleration": 12.5, "sdk_product_launches": 8.0, "sponsor_activity": 7.5, "social_discussion": 8.0, "funding_activity": 3.5, "competition_opportunity": 7.5},
        "tracked_repos": ["stacks-network/stacks-core"],
        "notes": "Nakamoto upgrade delivering 5-second fast blocks and 1:1 Bitcoin-backed asset sBTC smart contracts.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "rootstock",
        "name": "Rootstock",
        "category": "Merged-Mined Bitcoin L2",
        "momentum_score": 74.0,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 15.0, "hackathons_and_grants": 15.0, "dev_activity_acceleration": 11.5, "sdk_product_launches": 7.0, "sponsor_activity": 7.0, "social_discussion": 7.0, "funding_activity": 3.5, "competition_opportunity": 8.0},
        "tracked_repos": ["rsksmart/rskj"],
        "notes": "Longest-standing Bitcoin smart contract platform secured by over 50% of Bitcoin's hashing power via merged mining.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "bittensor",
        "name": "Bittensor",
        "category": "Decentralized AI Subnets",
        "momentum_score": 91.0,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 19.0, "hackathons_and_grants": 18.5, "dev_activity_acceleration": 14.5, "sdk_product_launches": 9.0, "sponsor_activity": 8.5, "social_discussion": 9.5, "funding_activity": 4.5, "competition_opportunity": 7.5},
        "tracked_repos": ["opentensor/bittensor"],
        "notes": "Decentralized commodity machine intelligence markets where specialized subnets compete and get rewarded via Yuma Consensus.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "asi-alliance",
        "name": "Fetch.ai / ASI Alliance",
        "category": "Autonomous AI Agents",
        "momentum_score": 83.0,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 17.0, "hackathons_and_grants": 17.0, "dev_activity_acceleration": 12.5, "sdk_product_launches": 8.5, "sponsor_activity": 8.0, "social_discussion": 8.5, "funding_activity": 4.0, "competition_opportunity": 7.5},
        "tracked_repos": ["fetchai/uAgents"],
        "notes": "Formed through merger of Fetch.ai, SingularityNET, and Ocean Protocol to develop open decentralized artificial general intelligence.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "render-network",
        "name": "Render Network",
        "category": "Decentralized GPU Compute",
        "momentum_score": 84.0,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 17.0, "hackathons_and_grants": 17.0, "dev_activity_acceleration": 13.0, "sdk_product_launches": 8.5, "sponsor_activity": 8.5, "social_discussion": 8.5, "funding_activity": 4.0, "competition_opportunity": 7.5},
        "tracked_repos": ["rendernetwork"],
        "notes": "Solana-migrated distributed GPU rendering and AI model training network connecting node operators with compute buyers.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "virtuals-protocol",
        "name": "Virtuals Protocol",
        "category": "Co-Owned AI Agents",
        "momentum_score": 87.5,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 18.0, "hackathons_and_grants": 18.0, "dev_activity_acceleration": 13.5, "sdk_product_launches": 9.0, "sponsor_activity": 8.0, "social_discussion": 9.5, "funding_activity": 4.0, "competition_opportunity": 6.5},
        "tracked_repos": ["virtuals-protocol"],
        "notes": "Leading the onchain AI agent launchpad meta on Base with autonomous social agents and multi-modal revenue sharing.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "sentient",
        "name": "Sentient",
        "category": "Open-Source AGI Foundation",
        "momentum_score": 82.0,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 17.0, "hackathons_and_grants": 17.5, "dev_activity_acceleration": 12.5, "sdk_product_launches": 8.0, "sponsor_activity": 8.0, "social_discussion": 8.5, "funding_activity": 4.5, "competition_opportunity": 6.0},
        "tracked_repos": ["sentient-agi"],
        "notes": "Raised $85M to build open-source AGI models with cryptographic economic incentives for AI researchers and contributors.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "gensyn",
        "name": "Gensyn",
        "category": "Machine Learning Compute Protocol",
        "momentum_score": 83.5,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 17.5, "hackathons_and_grants": 17.0, "dev_activity_acceleration": 13.0, "sdk_product_launches": 8.5, "sponsor_activity": 8.0, "social_discussion": 8.5, "funding_activity": 4.5, "competition_opportunity": 6.5},
        "tracked_repos": ["gensyn-ai"],
        "notes": "Cryptographic verification protocol for deep learning compute, enabling trustless distributed training without trusted execution.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "ocean-protocol",
        "name": "Ocean Protocol",
        "category": "Decentralized Data & AI",
        "momentum_score": 79.0,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 16.0, "hackathons_and_grants": 16.0, "dev_activity_acceleration": 12.0, "sdk_product_launches": 8.0, "sponsor_activity": 7.5, "social_discussion": 8.0, "funding_activity": 3.5, "competition_opportunity": 8.0},
        "tracked_repos": ["oceanprotocol/ocean.py"],
        "notes": "Tokenizes AI datasets and compute-to-data algorithms, allowing private data monetization without sharing raw files.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "akash-network",
        "name": "Akash Network",
        "category": "Decentralized Cloud Marketplace",
        "momentum_score": 82.5,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 17.0, "hackathons_and_grants": 17.0, "dev_activity_acceleration": 13.0, "sdk_product_launches": 8.5, "sponsor_activity": 8.0, "social_discussion": 8.0, "funding_activity": 3.5, "competition_opportunity": 7.5},
        "tracked_repos": ["akash-network/node"],
        "notes": "Cosmos-based open-source Supercloud marketplace for high-density GPUs (H100/A100) at 70-80% discount to AWS.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "the-graph",
        "name": "The Graph",
        "category": "Decentralized Indexing & Query",
        "momentum_score": 81.5,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 17.0, "hackathons_and_grants": 16.5, "dev_activity_acceleration": 12.5, "sdk_product_launches": 8.5, "sponsor_activity": 8.5, "social_discussion": 7.5, "funding_activity": 3.5, "competition_opportunity": 7.5},
        "tracked_repos": ["graphprotocol/graph-node"],
        "notes": "The indexing backbone of Web3 expanding into subgraphs, AI query assist, and generalized verifiable data services.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "grass",
        "name": "Grass",
        "category": "Decentralized Web Crawling / DePIN",
        "momentum_score": 85.0,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 17.5, "hackathons_and_grants": 17.5, "dev_activity_acceleration": 13.5, "sdk_product_launches": 8.5, "sponsor_activity": 8.0, "social_discussion": 9.5, "funding_activity": 4.0, "competition_opportunity": 6.5},
        "tracked_repos": ["getgrass-io"],
        "notes": "Converts residential bandwidth into a distributed web scraping network collecting clean training data for AI models.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "iexec",
        "name": "iExec",
        "category": "Confidential Computing / TEE",
        "momentum_score": 77.0,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 15.5, "hackathons_and_grants": 15.5, "dev_activity_acceleration": 12.0, "sdk_product_launches": 7.5, "sponsor_activity": 7.5, "social_discussion": 7.5, "funding_activity": 3.5, "competition_opportunity": 8.0},
        "tracked_repos": ["iExecBlockchainComputing"],
        "notes": "Confidential computing platform using Intel SGX hardware enclaves to execute privacy-preserving decentralized AI workflows.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "oasis-network",
        "name": "Oasis Network",
        "category": "Privacy-First Sapphire EVM",
        "momentum_score": 79.5,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 16.5, "hackathons_and_grants": 16.0, "dev_activity_acceleration": 12.5, "sdk_product_launches": 8.0, "sponsor_activity": 7.5, "social_discussion": 8.0, "funding_activity": 3.5, "competition_opportunity": 7.5},
        "tracked_repos": ["oasisprotocol/oasis-core"],
        "notes": "Sapphire confidential EVM runtime enabling confidential smart contracts, onchain key management, and private AI agent state.",
        "maturity_stage": "emerging"
    },
    {
        "slug": "autonolas",
        "name": "Autonolas (Olas)",
        "category": "Offchain Autonomous Agent Economy",
        "momentum_score": 83.5,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 17.5, "hackathons_and_grants": 17.0, "dev_activity_acceleration": 13.0, "sdk_product_launches": 8.5, "sponsor_activity": 8.0, "social_discussion": 8.5, "funding_activity": 4.0, "competition_opportunity": 7.0},
        "tracked_repos": ["valory-xyz/open-autonomy"],
        "notes": "Open Autonomy framework powering decentralized co-owned autonomous agent services across Gnosis, Base, and Polygon.",
        "maturity_stage": "emerging"
    },

    # --- WATCHLIST (10) ---
    {
        "slug": "citrea",
        "name": "Citrea",
        "category": "Bitcoin ZK Rollup",
        "momentum_score": 68.0,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 14.0, "hackathons_and_grants": 14.5, "dev_activity_acceleration": 11.5, "sdk_product_launches": 7.0, "sponsor_activity": 6.5, "social_discussion": 7.5, "funding_activity": 3.5, "competition_opportunity": 3.5},
        "tracked_repos": ["chainwayxyz/citrea"],
        "notes": "First ZK Rollup on Bitcoin using BitVM to verify validity proofs directly within Bitcoin Script.",
        "maturity_stage": "watchlist"
    },
    {
        "slug": "botanix",
        "name": "Botanix",
        "category": "Spiderchain Bitcoin EVM",
        "momentum_score": 65.0,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 13.5, "hackathons_and_grants": 13.5, "dev_activity_acceleration": 11.0, "sdk_product_launches": 6.5, "sponsor_activity": 6.5, "social_discussion": 7.0, "funding_activity": 3.5, "competition_opportunity": 3.5},
        "tracked_repos": ["botanix-labs"],
        "notes": "Decentralized Spiderchain multi-signature network enabling pure Bitcoin-native EVM smart contracts.",
        "maturity_stage": "watchlist"
    },
    {
        "slug": "bitlayer",
        "name": "Bitlayer",
        "category": "BitVM-Based Bitcoin L2",
        "momentum_score": 67.5,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 14.0, "hackathons_and_grants": 14.0, "dev_activity_acceleration": 11.5, "sdk_product_launches": 7.0, "sponsor_activity": 6.5, "social_discussion": 7.5, "funding_activity": 3.5, "competition_opportunity": 3.5},
        "tracked_repos": ["bitlayer-org"],
        "notes": "Secured by BitVM optimistic execution and equivalence proof model with growing Asian ecosystem developer builder grants.",
        "maturity_stage": "watchlist"
    },
    {
        "slug": "mezo",
        "name": "Mezo",
        "category": "Bitcoin Economic Layer",
        "momentum_score": 66.0,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 13.5, "hackathons_and_grants": 13.5, "dev_activity_acceleration": 11.0, "sdk_product_launches": 6.5, "sponsor_activity": 7.0, "social_discussion": 7.5, "funding_activity": 3.5, "competition_opportunity": 3.5},
        "tracked_repos": ["mezo-org"],
        "notes": "Built by Thesis team (Keep, Fold) as a permissionless Bitcoin economic layer utilizing Proof-of-HODL consensus.",
        "maturity_stage": "watchlist"
    },
    {
        "slug": "hashkey-chain",
        "name": "HashKey Chain",
        "category": "Compliant Institutional L2",
        "momentum_score": 64.0,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 13.0, "hackathons_and_grants": 13.0, "dev_activity_acceleration": 10.5, "sdk_product_launches": 6.5, "sponsor_activity": 7.0, "social_discussion": 7.0, "funding_activity": 3.5, "competition_opportunity": 3.5},
        "tracked_repos": ["hashkey"],
        "notes": "Licensed exchange ecosystem rollup bringing institutional Asian capital, RWAs, and compliant fintech into Web3.",
        "maturity_stage": "watchlist"
    },
    {
        "slug": "logos",
        "name": "Logos",
        "category": "Grassroots Privacy & Cypherpunk Stack",
        "momentum_score": 62.5,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 13.0, "hackathons_and_grants": 12.5, "dev_activity_acceleration": 10.5, "sdk_product_launches": 6.5, "sponsor_activity": 6.0, "social_discussion": 7.0, "funding_activity": 3.5, "competition_opportunity": 3.5},
        "tracked_repos": ["logos-co"],
        "notes": "Cypherpunk political and technological stack uniting Waku (messaging), Codex (storage), and Nomos (consensus).",
        "maturity_stage": "watchlist"
    },
    {
        "slug": "zero-gravity",
        "name": "0G (ZeroGravity)",
        "category": "Modular AI Data Availability",
        "momentum_score": 69.5,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 14.5, "hackathons_and_grants": 14.5, "dev_activity_acceleration": 12.0, "sdk_product_launches": 7.0, "sponsor_activity": 7.0, "social_discussion": 7.5, "funding_activity": 4.0, "competition_opportunity": 3.0},
        "tracked_repos": ["0glabs"],
        "notes": "Modular AI data availability layer designed to feed high-bandwidth model weights and training datasets to onchain smart contracts.",
        "maturity_stage": "watchlist"
    },
    {
        "slug": "blast",
        "name": "Blast",
        "category": "Native Yield L2",
        "momentum_score": 68.5,
        "momentum_trajectory": "↓",
        "breakdown_scores": {"developer_programs": 14.0, "hackathons_and_grants": 14.0, "dev_activity_acceleration": 11.0, "sdk_product_launches": 7.0, "sponsor_activity": 7.0, "social_discussion": 7.5, "funding_activity": 3.5, "competition_opportunity": 4.5},
        "tracked_repos": ["blast-io"],
        "notes": "Built-in rebasing yields for ETH and stablecoins with high early retail adoption transitioning into developer sustainability.",
        "maturity_stage": "watchlist"
    },
    {
        "slug": "metis",
        "name": "Metis",
        "category": "Decentralized Sequencer L2",
        "momentum_score": 67.0,
        "momentum_trajectory": "→",
        "breakdown_scores": {"developer_programs": 13.5, "hackathons_and_grants": 14.0, "dev_activity_acceleration": 11.0, "sdk_product_launches": 6.5, "sponsor_activity": 7.0, "social_discussion": 7.5, "funding_activity": 3.5, "competition_opportunity": 4.0},
        "tracked_repos": ["metis-edu"],
        "notes": "First Ethereum rollup to operationalize a decentralized sequencer pool with continuous ecosystem grant incentives.",
        "maturity_stage": "watchlist"
    },
    {
        "slug": "decentralized-ai",
        "name": "Decentralized AI Subnets",
        "category": "Subnet & Agent Ecosystems",
        "momentum_score": 93.0,
        "momentum_trajectory": "↑",
        "breakdown_scores": {"developer_programs": 19.5, "hackathons_and_grants": 19.0, "dev_activity_acceleration": 14.5, "sdk_product_launches": 9.5, "sponsor_activity": 9.0, "social_discussion": 9.5, "funding_activity": 4.5, "competition_opportunity": 7.5},
        "tracked_repos": ["opentensor/bittensor", "virtuals-protocol", "myshell-ai"],
        "notes": "Umbrella intelligence category capturing the explosive migration of AI engineers into crypto-incentivized subnet coordination.",
        "maturity_stage": "watchlist"
    }
]

# --------------------------------------------------------------------------- #
#                        2. SPONSOR PROFILES (ENGINE 3)                       #
# --------------------------------------------------------------------------- #

SEED_SPONSORS: List[Dict[str, Any]] = [
    {
        "slug": "world",
        "name": "World (Worldcoin)",
        "ecosystem": "World Chain / Ethereum",
        "technology": "World ID, MiniKit, ZK Human Verification",
        "predictability_score": 92.0,
        "upcoming_likelihood": 95.0,
        "previous_hackathons": ["ETHGlobal Brussels", "ETHGlobal Singapore", "ETHGlobal San Francisco", "ETHGlobal Bangkok"],
        "prize_amounts_total": 120000.0,
        "tracks": ["Best World ID Integration", "Best Mini App for World App", "Sybil-Resistant Governance"],
        "bounties": ["$5,000 Top World ID Mini App", "$2,500 Best ZK Proof Usage", "$1,000 Pool Prize"],
        "recurring_technologies": ["MiniKit SDK", "World ID IDKit", "Nullifier hash verification", "Next.js / React"],
        "recurring_bounty_categories": ["Mini Apps", "Sybil resistance", "Biometric verification", "Social graphs"],
        "common_winning_product_types": ["Mobile-friendly mini-apps", "Human-gated agent escrow", "Fair-launch token distributions"],
        "features_frequently_used": ["IDKit verify widget", "App level credential verification"],
        "features_rarely_used": ["On-chain stateful nullifier verification with smart contracts", "Off-chain server-side verification"],
        "oversaturated_ideas": ["Generic proof-of-humanity voting polls", "Simple login buttons without ongoing state"],
        "underserved_ideas": ["Autonomous AI agent safety gates where high-risk actions require human biometric nullifier attestation", "Private sybil-resistant developer review systems"],
        "integration_difficulty": "Low",
        "documentation_quality": "Exceptional",
        "typical_prize_distribution": "$5k / $2.5k / $1.5k tier with a generous $5k pooled prize for all qualifying teams.",
        "historical_participation_rewards": "Frequently pays out $250-$500 pool rewards to any project with a working IDKit proof.",
        "repeat_sponsorship_frequency": "Universal across ETHGlobal circuit (present in 9 of last 10 major events).",
        "recommended_preparation": "Clone World MiniKit template, test local mock verification, and build nullifier replay protection beforehand."
    },
    {
        "slug": "dynamic",
        "name": "Dynamic",
        "ecosystem": "Multi-chain (EVM, Solana, Bitcoin)",
        "technology": "Embedded Wallets, Multi-Chain Auth, Session Keys",
        "predictability_score": 88.0,
        "upcoming_likelihood": 90.0,
        "previous_hackathons": ["ETHGlobal San Francisco", "ETHGlobal Brussels", "ETHOnline", "Solana Renaissance"],
        "prize_amounts_total": 85000.0,
        "tracks": ["Best Embedded Wallet UX", "Most Innovative Auth Flow", "Multi-Chain Identity"],
        "bounties": ["$4,000 1st Place", "$2,000 2nd Place", "$1,000 Pool Prize"],
        "recurring_technologies": ["@dynamic-labs/sdk-react-core", "Wagmi connector", "Embedded session keys"],
        "recurring_bounty_categories": ["Social login onboarding", "Gasless transaction flows", "Multi-wallet linking"],
        "common_winning_product_types": ["Consumer apps hiding crypto complexity", "Agentic wallets with scoped permissions"],
        "features_frequently_used": ["Standard Google/Twitter social login popup"],
        "features_rarely_used": ["Scoped session keys for autonomous agents", "Cross-chain linked account signatures"],
        "oversaturated_ideas": ["Basic web3 storefront with email login"],
        "underserved_ideas": ["Autonomous AI agents operating with pre-approved Dynamic session keys and spending limits"],
        "integration_difficulty": "Low",
        "documentation_quality": "Exceptional",
        "typical_prize_distribution": "$4k / $2k with $1k pooled prize.",
        "historical_participation_rewards": "Pool rewards for clean multi-chain auth integration.",
        "repeat_sponsorship_frequency": "Present at almost every major ETHGlobal and multi-chain hackathon.",
        "recommended_preparation": "Set up Dynamic environment API key, pre-configure Wagmi / Viem hooks, test embedded session key signing."
    },
    {
        "slug": "pyth-network",
        "name": "Pyth Network",
        "ecosystem": "Solana / Multi-chain Oracles",
        "technology": "Pull Oracles, Real-Time Low-Latency Feeds, Pyth Entropy",
        "predictability_score": 90.0,
        "upcoming_likelihood": 85.0,
        "previous_hackathons": ["Solana Radar", "ETHGlobal Singapore", "Monad Madness", "Sui Overflow"],
        "prize_amounts_total": 110000.0,
        "tracks": ["Best Use of Pyth Price Feeds", "Best Use of Pyth Entropy (RNG)", "DeFi / Cross-Chain Innovation"],
        "bounties": ["$5,000 Best DeFi App", "$3,000 Best Consumer App with Entropy", "$2,000 Pool"],
        "recurring_technologies": ["Pyth Hermes client", "Pull oracle SDK", "Pyth Entropy smart contract bindings"],
        "recurring_bounty_categories": ["Perpetuals / Derivatives", "Predictive markets", "Verifiable onchain gaming / RNG"],
        "common_winning_product_types": ["Low-latency liquidation engines", "Fair onchain lotteries / gaming with Entropy"],
        "features_frequently_used": ["Standard crypto asset price feed queries"],
        "features_rarely_used": ["Pyth Benchmarks historical price feeds", "Pyth Entropy for non-gaming cryptographic randomness"],
        "oversaturated_ideas": ["Simple lending app mockups with standard price feeds"],
        "underserved_ideas": ["Autonomous liquidation bots running on parallel execution chains with sub-second Hermes price updates"],
        "integration_difficulty": "Medium",
        "documentation_quality": "Good",
        "typical_prize_distribution": "$5k / $3k / $2k pool.",
        "historical_participation_rewards": "Consistently rewards teams implementing Hermes on testnet.",
        "repeat_sponsorship_frequency": "High across both Solana and EVM hackathons.",
        "recommended_preparation": "Learn the pull-oracle model (updating price feeds on-demand in the same transaction) via Hermes."
    }
]

# --------------------------------------------------------------------------- #
#                        3. HISTORICAL WINNERS (ENGINE 4)                     #
# --------------------------------------------------------------------------- #

SEED_WINNERS: List[Dict[str, Any]] = [
    {
        "id": "win_agent_escrow_2025",
        "opportunity_id": "colosseum-crypto-worlds-fair-2026",
        "event_name": "Solana Radar Hackathon",
        "project_name": "KitePay — Autonomous Agent Rail",
        "category": "DeFi / AI Agents",
        "problem_solved": "AI agents had no standardized way to pay each other for API calls without exposing private keys.",
        "product_category": "infra",
        "infra_vs_consumer": "Infrastructure",
        "frontend_quality": "High",
        "ux_quality": "Clean streaming terminal UI with live balance updates",
        "technical_depth": "Exceptional",
        "sponsor_integration_depth": "Deep",
        "originality": "High",
        "demo_quality": "Flawless live demo of agent buying compute from another agent",
        "github_quality": "Clean Rust program + TypeScript client + Docker compose",
        "number_of_integrations": 3,
        "ai_usage": 1,
        "privacy_usage": 0,
        "financial_use_case": 1,
        "judges": "Toly, Chris Heaney, Raj Gokal",
        "prize_won": "$50,000 (1st Place Tracks)",
        "repo_url": "https://github.com/example/kitepay",
        "demo_url": "https://youtu.be/example",
        "winning_patterns": "Solved real friction point; live agent-to-agent streaming demo; deep Anchor smart contract integration.",
        "losing_patterns_identified": "Competitors submitted static slide decks with mock transactions that failed during live testing.",
        "oversaturated_category": 0
    },
    {
        "id": "win_zk_guardian_2025",
        "opportunity_id": "colosseum-crypto-worlds-fair-2026",
        "event_name": "ETHGlobal Brussels",
        "project_name": "GuardianNull — Biometric Agent Guardrails",
        "category": "AI / Security",
        "problem_solved": "Prevented autonomous trading agents from suffering rogue prompt injections and draining wallets.",
        "product_category": "devtool",
        "infra_vs_consumer": "Infrastructure",
        "frontend_quality": "High",
        "ux_quality": "Dual-pane dashboard showing prompt injection on left and ZK-nullifier biometric block on right",
        "technical_depth": "High",
        "sponsor_integration_depth": "Deep",
        "originality": "High",
        "demo_quality": "Live attack demonstration mitigated in real-time",
        "github_quality": "Complete monorepo with FastAPI + Next.js + World ID contract",
        "number_of_integrations": 2,
        "ai_usage": 1,
        "privacy_usage": 1,
        "financial_use_case": 0,
        "judges": "World Foundation & ETHGlobal Curators",
        "prize_won": "$12,500 (World ID Track Winner + Finalist)",
        "repo_url": "https://github.com/example/guardian-null",
        "demo_url": "https://youtu.be/example2",
        "winning_patterns": "Deep World ID nullifier integration; visual live demo contrasting attack vs defense.",
        "losing_patterns_identified": "Teams that just put a 'Login with World ID' button on a generic website did not place.",
        "oversaturated_category": 0
    }
]

# --------------------------------------------------------------------------- #
#                     4. ACTIVE OPPORTUNITIES (ENGINE 1, 5, 6)                #
# --------------------------------------------------------------------------- #

SEED_OPPORTUNITIES: List[Dict[str, Any]] = [
    {
        "id": "colosseum-crypto-worlds-fair-2026",
        "name": "Colosseum Crypto World's Fair 2026",
        "slug": "colosseum-crypto-worlds-fair-2026",
        "type": "hackathon",
        "organizer": "Colosseum",
        "ecosystem": "Solana / Base / Ethereum / Sui / Zcash / Bitcoin / Tempo",
        "registration_open": True,
        "registration_deadline": "2026-10-05T23:59:59Z",
        "submission_deadline": "2026-10-12T23:59:59Z",
        "total_prize_usd": 3340000.0,
        "prize_breakdown": {
            "grand_prize": 100000.0,
            "accelerator_investments": 2500000.0,
            "ecosystem_tracks": 740000.0
        },
        "tracks": ["AI & Autonomous Agents", "Consumer & Payments", "DeFi & Capital Markets", "Infrastructure & DePIN", "Privacy & ZK"],
        "sponsors": ["Solana Foundation", "Base", "Sui Foundation", "Zcash Open Source", "Tempo"],
        "participation_rewards": "Exclusive developer Discord access, testnet RPC vouchers, and direct Colosseum accelerator consideration for all qualifying submissions.",
        "expected_competitors": 2200,
        "prize_to_competitor_ratio": 5422.08,
        "prob_placing": 0.45,
        "prob_any_reward": 0.75,
        "hack_score": 94.2,
        "skill_match_score": 84.7,
        "score_breakdown": {
            "reward_quality": 20.0,
            "competition_attractiveness": 20.0,
            "skill_fit": 12.7,
            "sponsor_history": 9.0,
            "ecosystem_momentum": 9.5,
            "prize_breadth": 10.0,
            "participation_rewards": 5.0,
            "startup_potential": 5.0,
            "portfolio_value": 4.5
        },
        "alert_level": 3,
        "status": "confirmed",
        "url": "https://www.colosseum.org/worlds-fair",
        "source_tier": "Tier 1",
        "source_url": "https://www.colosseum.org/news/announcing-crypto-worlds-fair",
        "tags": ["AI Agents", "Payments", "Solana", "Base", "DePIN", "Consumer"],
        "recommended_build_direction": {
            "what_everyone_else_will_build": "A generic Telegram trading bot with basic price alerts or a toy token launchpad.",
            "your_unfair_advantage_build": "Autonomous Agent x402 Micropayment Gateway: Combine your FastAPI high-concurrency engine with an x402 reverse proxy. AI agents querying your endpoints pay micro-tokens per LLM inference call on Solana/Base. Use hackathon-launchpad's dual-pane canvas to show live transaction proofs on the left and streaming LLM token generation on the right."
        },
        "technologies_to_learn": ["Solana Web3.js / Anchor client basics or Python Solana RPC", "World ID MiniKit SDK / Coinbase AgentKit Python", "HTTP 402 Payment Required header signing & facilitator specs"]
    },
    {
        "id": "monad-metropolis-nitro-2026",
        "name": "Monad Metropolis & Nitro Accelerator Cohort 2",
        "slug": "monad-metropolis-nitro-2026",
        "type": "accelerator",
        "organizer": "Monad Foundation",
        "ecosystem": "Monad",
        "registration_open": True,
        "registration_deadline": "2026-10-15T23:59:59Z",
        "submission_deadline": "2026-10-31T23:59:59Z",
        "total_prize_usd": 750000.0,
        "prize_breakdown": {
            "nitro_investment": 500000.0,
            "grant_pool": 250000.0
        },
        "tracks": ["Parallel Execution High-Throughput DeFi", "AI Model Serving & Inference Verification", "Real-Time Gaming"],
        "sponsors": ["Monad Labs", "Paradigm", "Dragonfly"],
        "participation_rewards": "1:1 token matching pool for all teams deployed on Monad testnet.",
        "expected_competitors": 950,
        "prize_to_competitor_ratio": 2819.55,
        "prob_placing": 0.45,
        "prob_any_reward": 0.75,
        "hack_score": 90.8,
        "skill_match_score": 85.2,
        "score_breakdown": {
            "reward_quality": 18.5,
            "competition_attractiveness": 20.0,
            "skill_fit": 12.8,
            "sponsor_history": 8.5,
            "ecosystem_momentum": 9.0,
            "prize_breadth": 8.0,
            "participation_rewards": 5.0,
            "startup_potential": 5.0,
            "portfolio_value": 4.5
        },
        "alert_level": 3,
        "status": "confirmed",
        "url": "https://monad.xyz/nitro",
        "source_tier": "Tier 1",
        "source_url": "https://monad.xyz/blog/nitro-accelerator-cohort-2",
        "tags": ["Parallel EVM", "High Throughput", "AI Inference", "Nitro"],
        "recommended_build_direction": {
            "what_everyone_else_will_build": "A standard Uniswap v2 fork or basic EVM contract re-deployed on testnet with no performance differentiation.",
            "your_unfair_advantage_build": "Parallel EVM High-Throughput Model Benchmarking: Exploit Monad's 10,000 TPS parallel state execution to run continuous verifiable agent evaluations using Ragas/DeepEval with real-time SSE telemetry."
        },
        "technologies_to_learn": ["Monad parallel execution RPC and testnet contracts"]
    },
    {
        "id": "base-retroactive-builder-grants-2026",
        "name": "Base Retroactive Builder Grants & Base Batches",
        "slug": "base-retroactive-builder-grants-2026",
        "type": "grant",
        "organizer": "Base Foundation",
        "ecosystem": "Base",
        "registration_open": True,
        "registration_deadline": "Rolling",
        "submission_deadline": "Ongoing / Bi-weekly",
        "total_prize_usd": 500000.0,
        "prize_breakdown": {
            "builder_grants": 300000.0,
            "base_batches_capital": 200000.0
        },
        "tracks": ["Agentic Commerce (x402)", "Smart Wallet Onboarding", "Onchain Social & Media"],
        "sponsors": ["Coinbase Ventures", "Base Core Team"],
        "participation_rewards": "1-5 ETH retroactive grants for every project with verified testnet or mainnet contracts and active user transactions.",
        "expected_competitors": 450,
        "prize_to_competitor_ratio": 3968.25,
        "prob_placing": 0.45,
        "prob_any_reward": 0.75,
        "hack_score": 87.8,
        "skill_match_score": 82.0,
        "score_breakdown": {
            "reward_quality": 16.5,
            "competition_attractiveness": 20.0,
            "skill_fit": 12.3,
            "sponsor_history": 9.5,
            "ecosystem_momentum": 9.5,
            "prize_breadth": 6.0,
            "participation_rewards": 5.0,
            "startup_potential": 4.5,
            "portfolio_value": 4.5
        },
        "alert_level": 3,
        "status": "active",
        "url": "https://base.mirror.xyz",
        "source_tier": "Tier 1",
        "source_url": "https://warpcast.com/jessepollak",
        "tags": ["Base", "x402", "AgentKit", "Smart Wallet", "Grants"],
        "recommended_build_direction": {
            "what_everyone_else_will_build": "A basic NFT frame or simple social tipping bot with mock transaction confirmations.",
            "your_unfair_advantage_build": "Verifiable Agentic Commerce Hub: Use Coinbase AgentKit and ERC-8021 builder codes with an autonomous semantic evaluation cache, routing high-frequency micro-settlements across Base."
        },
        "technologies_to_learn": ["World ID MiniKit SDK / Coinbase AgentKit Python", "HTTP 402 Payment Required header signing & facilitator specs"]
    },
    {
        "id": "ethglobal-tokyo-2026",
        "name": "ETHGlobal Tokyo 2026",
        "slug": "ethglobal-tokyo-2026",
        "type": "hackathon",
        "organizer": "ETHGlobal",
        "ecosystem": "Ethereum / L2s",
        "registration_open": True,
        "registration_deadline": "2026-09-24T23:59:59Z",
        "submission_deadline": "2026-09-27T12:00:00Z",
        "total_prize_usd": 150000.0,
        "prize_breakdown": {
            "finalist_prizes": 25000.0,
            "sponsor_bounties": 125000.0
        },
        "tracks": ["Layer 2 Scale", "AI x Crypto", "Account Abstraction", "Public Goods"],
        "sponsors": ["World", "Dynamic", "Pyth Network", "Uniswap Foundation", "Arbitrum", "Optimism"],
        "participation_rewards": "Extensive pooled sponsor prizes ($250-$1,000 for qualifying submissions using sponsor SDKs).",
        "expected_competitors": 800,
        "prize_to_competitor_ratio": 669.64,
        "prob_placing": 0.45,
        "prob_any_reward": 0.75,
        "hack_score": 88.0,
        "skill_match_score": 89.0,
        "score_breakdown": {
            "reward_quality": 16.5,
            "competition_attractiveness": 17.5,
            "skill_fit": 13.4,
            "sponsor_history": 9.5,
            "ecosystem_momentum": 8.6,
            "prize_breadth": 10.0,
            "participation_rewards": 5.0,
            "startup_potential": 4.0,
            "portfolio_value": 4.5
        },
        "alert_level": 3,
        "status": "confirmed",
        "url": "https://ethglobal.com/events/tokyo2026",
        "source_tier": "Tier 2",
        "source_url": "https://ethglobal.com/events/tokyo2026",
        "tags": ["ETHGlobal", "Ethereum", "World ID", "Dynamic", "Pyth", "AI Agents"],
        "recommended_build_direction": {
            "what_everyone_else_will_build": "A simple World ID login button or generic proof-of-humanity voting mockup.",
            "your_unfair_advantage_build": "Human-Guarded Autonomous Agent Escrow: Deploy a LangGraph multi-agent team with NeMo Guardrails managing onchain treasuries, requiring World ID nullifier biometric proofs only when spending limits or anomalous tool calls trigger escalation. Deep integration with World ID MiniKit."
        },
        "technologies_to_learn": ["World ID MiniKit SDK / Coinbase AgentKit Python", "Dynamic embedded session keys"]
    },
    {
        "id": "keeperhub-agent-economy-hackathon-2026",
        "name": "KeeperHub - The Agent Economy Hackathon",
        "slug": "keeperhub-agent-economy-hackathon-2026",
        "type": "hackathon",
        "organizer": "DoraHacks",
        "ecosystem": "Multi-chain (EVM, Solana)",
        "registration_open": True,
        "registration_deadline": "2026-09-18T23:59:59Z",
        "submission_deadline": "2026-09-20T23:59:59Z",
        "total_prize_usd": 65000.0,
        "prize_breakdown": {
            "1st_prize": 20000.0,
            "2nd_prize": 12000.0,
            "3rd_prize": 8000.0,
            "bounty_tracks": 25000.0
        },
        "tracks": ["Autonomous Agent Orchestration", "Agentic Micro-Payments", "Evaluation & Guardrails for Web3 Agents"],
        "sponsors": ["KeeperDAO", "Virtuals Protocol", "Solana Foundation"],
        "participation_rewards": "Fast-track incubation and GPU credit grants from sponsor compute clusters.",
        "expected_competitors": 280,
        "prize_to_competitor_ratio": 833.33,
        "prob_placing": 0.45,
        "prob_any_reward": 0.75,
        "hack_score": 81.4,
        "skill_match_score": 86.0,
        "score_breakdown": {
            "reward_quality": 14.5,
            "competition_attractiveness": 17.0,
            "skill_fit": 12.9,
            "sponsor_history": 8.0,
            "ecosystem_momentum": 8.5,
            "prize_breadth": 7.0,
            "participation_rewards": 4.0,
            "startup_potential": 3.5,
            "portfolio_value": 4.0
        },
        "alert_level": 3,
        "status": "confirmed",
        "url": "https://dorahacks.io/hackathon/keeperhub",
        "source_tier": "Tier 2",
        "source_url": "https://dorahacks.io",
        "tags": ["AI Agents", "DoraHacks", "FastAPI", "Evaluation", "KeeperDAO"],
        "recommended_build_direction": {
            "what_everyone_else_will_build": "A generic LangChain query agent that fetches token balances from an RPC endpoint.",
            "your_unfair_advantage_build": "Autonomous Agent x402 Micropayment Gateway: Combine your FastAPI high-concurrency engine with an x402 reverse proxy. AI agents querying your endpoints pay micro-tokens per LLM inference call on Solana/Base. Use hackathon-launchpad's dual-pane canvas to show live transaction proofs on the left and streaming LLM token generation on the right."
        },
        "technologies_to_learn": ["Solana Web3.js / Anchor client basics or Python Solana RPC"]
    }
]

# --------------------------------------------------------------------------- #
#                        5. BENEFITS & PERKS (ENGINE 12)                      #
# --------------------------------------------------------------------------- #

SEED_BENEFITS: List[Dict[str, Any]] = [
    {
        "id": "benefit_ef_fellowships",
        "name": "Ethereum Foundation Academic & Research Fellowships",
        "provider": "Ethereum Foundation",
        "ecosystem": "Ethereum",
        "benefit_type": "fellowship",
        "typical_amount_usd": 65000.0,
        "rolling_or_deadline": "rolling",
        "eligibility_notes": "Open to developers and researchers working on cryptography, consensus mechanisms, client diversity, or developer tooling. Non-dilutive stipend.",
        "application_url": "https://esp.ethereum.foundation"
    },
    {
        "id": "benefit_op_retropgf",
        "name": "Optimism Retroactive Public Goods Funding (RetroPGF)",
        "provider": "Optimism Collective",
        "ecosystem": "Optimism / OP Superchain",
        "benefit_type": "retroactive_funding",
        "typical_amount_usd": 85000.0,
        "rolling_or_deadline": "rolling",
        "eligibility_notes": "Rewards developers who have already created demonstrable public goods, open-source repos, or educational infrastructure used by the OP Superchain.",
        "application_url": "https://app.optimism.io/retropgf"
    },
    {
        "id": "benefit_arbitrum_dao_grants",
        "name": "Arbitrum DAO Contributor & Growth Grants",
        "provider": "Arbitrum Foundation / DAO",
        "ecosystem": "Arbitrum",
        "benefit_type": "grant",
        "typical_amount_usd": 50000.0,
        "rolling_or_deadline": "rolling",
        "eligibility_notes": "Milestone-based non-dilutive grants for protocols, developer tools, and Arbitrum Orbit L3 infrastructure integrations.",
        "application_url": "https://arbitrum.foundation/grants"
    },
    {
        "id": "benefit_uniswap_grants",
        "name": "Uniswap Foundation Developer Grants Program",
        "provider": "Uniswap Foundation",
        "ecosystem": "Ethereum / Unichain",
        "benefit_type": "grant",
        "typical_amount_usd": 75000.0,
        "rolling_or_deadline": "rolling",
        "eligibility_notes": "Supports Uniswap v4 hook development, liquidity routing algorithms, and developer observability tooling.",
        "application_url": "https://www.uniswapfoundation.org/grants"
    },
    {
        "id": "benefit_polygon_fellowship",
        "name": "Polygon Village Fellowship & Builder Grants",
        "provider": "Polygon Foundation",
        "ecosystem": "Polygon",
        "benefit_type": "fellowship",
        "typical_amount_usd": 40000.0,
        "rolling_or_deadline": "rolling",
        "eligibility_notes": "Includes up to $40k grant vouchers, AWS/Google Cloud server credits, and dedicated audit support for AggLayer builders.",
        "application_url": "https://polygon.technology/village"
    },
    {
        "id": "benefit_w3f_grants",
        "name": "Web3 Foundation Open Grants Program",
        "provider": "Web3 Foundation",
        "ecosystem": "Polkadot",
        "benefit_type": "grant",
        "typical_amount_usd": 30000.0,
        "rolling_or_deadline": "rolling",
        "eligibility_notes": "Tiered non-dilutive grants (up to $30k for Tier 2) paid in crypto/USDC upon GitHub milestone completions for Polkadot SDK tools.",
        "application_url": "https://web3.foundation/grants"
    },
    {
        "id": "benefit_starknet_grants",
        "name": "Starknet Seed & Growth Tier Builder Grants",
        "provider": "Starknet Foundation",
        "ecosystem": "Starknet",
        "benefit_type": "grant",
        "typical_amount_usd": 50000.0,
        "rolling_or_deadline": "rolling",
        "eligibility_notes": "Seed grants up to $25k and Growth grants up to $50k in STRK tokens for teams deploying Cairo contracts and dev tools on mainnet.",
        "application_url": "https://starknet.io/grants"
    },
    {
        "id": "benefit_aptos_ecosystem_grants",
        "name": "Aptos Foundation Ecosystem & Payments Grants",
        "provider": "Aptos Foundation",
        "ecosystem": "Aptos",
        "benefit_type": "grant",
        "typical_amount_usd": 60000.0,
        "rolling_or_deadline": "rolling",
        "eligibility_notes": "Supports teams building Move financial primitives, autonomous agents, and low-friction mobile payment rails.",
        "application_url": "https://aptosfoundation.org/grants"
    },
    {
        "id": "benefit_solana_foundation_grants",
        "name": "Solana Foundation Direct Builder Grants",
        "provider": "Solana Foundation",
        "ecosystem": "Solana",
        "benefit_type": "grant",
        "typical_amount_usd": 45000.0,
        "rolling_or_deadline": "rolling",
        "eligibility_notes": "Fast-tracked non-dilutive grants for public goods, high-throughput RPC tools, and open-source developer libraries.",
        "application_url": "https://solana.org/grants"
    },
    {
        "id": "benefit_base_ecosystem_grants",
        "name": "Base Gas Rebates & Ecosystem Grants",
        "provider": "Base Core Team",
        "ecosystem": "Base",
        "benefit_type": "gas_credit",
        "typical_amount_usd": 25000.0,
        "rolling_or_deadline": "rolling",
        "eligibility_notes": "Offers gas credits and 1-5 ETH builder grants for contracts registered with ERC-8021 builder codes that drive active onchain volume.",
        "application_url": "https://base.org/builders"
    }
]

# --------------------------------------------------------------------------- #
#                   6. JOBS & INTERNSHIPS (ENGINE 13)                         #
# --------------------------------------------------------------------------- #

SEED_JOBS: List[Dict[str, Any]] = [
    {
        "id": "job_base_ai_engineer",
        "title": "Staff AI Platform Engineer (Autonomous Agents)",
        "company": "Base / Coinbase",
        "ecosystem_or_category": "Base / AI Infrastructure",
        "role_type": "full_time",
        "location": "Remote (US/Global)",
        "remote": True,
        "compensation_notes": "$210,000 - $260,000 + Equity + Incentive Grants",
        "first_seen": "2026-09-18T20:00:00Z",
        "application_deadline": "Rolling / Urgent",
        "url": "https://www.coinbase.com/careers",
        "skill_tags": ["Python", "FastAPI", "AgentKit", "LangGraph", "Docker", "Kubernetes", "vLLM"],
        "freshness_alert_sent": False
    },
    {
        "id": "job_world_zk_intern",
        "title": "AI & Cryptography Research Intern",
        "company": "Tools for Humanity (World)",
        "ecosystem_or_category": "World Chain / ZK",
        "role_type": "internship",
        "location": "San Francisco, CA or Remote",
        "remote": True,
        "compensation_notes": "$55 - $75 / hour + Housing Stipend",
        "first_seen": "2026-09-18T22:30:00Z",
        "application_deadline": "2026-10-31",
        "url": "https://world.org/careers",
        "skill_tags": ["Python", "PyTorch", "Zero-Knowledge", "World ID", "Math", "Algorithms"],
        "freshness_alert_sent": False
    },
    {
        "id": "job_paradigm_fellow",
        "title": "Research Fellow — High-Throughput & Parallel Systems",
        "company": "Paradigm",
        "ecosystem_or_category": "Monad / MegaETH / Research",
        "role_type": "fellowship",
        "location": "Remote / New York",
        "remote": True,
        "compensation_notes": "$150,000 fellowship grant + research computing budget",
        "first_seen": "2026-09-18T19:15:00Z",
        "application_deadline": "2026-10-15",
        "url": "https://www.paradigm.xyz",
        "skill_tags": ["Rust", "Python", "Parallel EVM", "Distributed Systems", "Performance"],
        "freshness_alert_sent": False
    },
    {
        "id": "job_solana_superteam_dev",
        "title": "Backend AI Infrastructure Engineer",
        "company": "Superteam / Solana Ecosystem",
        "ecosystem_or_category": "Solana",
        "role_type": "contract",
        "location": "Remote",
        "remote": True,
        "compensation_notes": "$8,000 - $12,000 / month (USDC)",
        "first_seen": "2026-09-18T23:00:00Z",
        "application_deadline": "Rolling",
        "url": "https://earn.superteam.fun",
        "skill_tags": ["Python", "FastAPI", "AsyncIO", "Solana", "Ray Serve", "Qdrant"],
        "freshness_alert_sent": False
    },
    {
        "id": "job_uniswap_entry_level",
        "title": "Junior Developer Tools Engineer",
        "company": "Uniswap Foundation",
        "ecosystem_or_category": "Ethereum / Unichain",
        "role_type": "entry_level",
        "location": "Remote",
        "remote": True,
        "compensation_notes": "$125,000 - $145,000 + Token Grant",
        "first_seen": "2026-09-18T18:00:00Z",
        "application_deadline": "Rolling",
        "url": "https://uniswap.org/careers",
        "skill_tags": ["TypeScript", "Python", "Smart Contracts", "APIs", "CLI"],
        "freshness_alert_sent": False
    }
]

# --------------------------------------------------------------------------- #
#                        7. TECHNICAL TRENDS (ENGINE 9)                       #
# --------------------------------------------------------------------------- #

SEED_TRENDS: List[Dict[str, Any]] = [
    {
        "id": "trend_x402_agent_payments",
        "narrative_name": "x402 HTTP Micro-Payments for AI Agents",
        "category": "AI Agents & Payments",
        "discussion_velocity": 96.0,
        "repository_growth": 91.0,
        "grants_moving": 92.0,
        "description": "Standardized HTTP 402 Payment Required headers allowing autonomous agents to pay for inference APIs, compute, and data via micro-tokens on Base/Solana.",
        "key_ecosystems": ["Base", "Solana", "Ethereum"],
        "actionable_implications": "Integrate an x402 reverse-proxy header into FastAPI backends. Judges immediately recognize and reward this as real infrastructure."
    },
    {
        "id": "trend_parallel_evm",
        "narrative_name": "Parallel Execution EVM (Monad / MegaETH)",
        "category": "High-Throughput Execution",
        "discussion_velocity": 92.0,
        "repository_growth": 88.0,
        "grants_moving": 94.0,
        "description": "Moving beyond single-threaded EVM execution by introducing parallel transaction processing and specialized state storage engines (10k-100k TPS).",
        "key_ecosystems": ["Monad", "MegaETH", "Sei"],
        "actionable_implications": "Build high-frequency settlement tools, continuous model evaluation telemetry, or parallel market engines that fail on standard EVMs."
    },
    {
        "id": "trend_verifiable_ai_inference",
        "narrative_name": "Verifiable Onchain Inference & TEE Guardrails",
        "category": "Decentralized AI & Security",
        "discussion_velocity": 89.0,
        "repository_growth": 85.0,
        "grants_moving": 90.0,
        "description": "Combining hardware TEEs (Trusted Execution Environments) and zero-knowledge proofs to prove that an AI model executed specific weights without tampering.",
        "key_ecosystems": ["Bittensor", "Sentient", "Oasis", "World Chain"],
        "actionable_implications": "Combine NeMo Guardrails / DeepEval evaluation traces with onchain cryptographic attestations for AI agent decisions."
    }
]
