import streamlit as st
import json
import os
from datetime import datetime
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(
    page_title="학생 테트리스 게임",
    page_icon="🎮",
    layout="wide"
)

# 점수 데이터 파일 경로
SCORES_FILE = "scores.json"

def load_scores():
    """점수 데이터 로드"""
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_score(name, mode, level, score, lines):
    """점수 저장"""
    scores = load_scores()
    new_score = {
        "timestamp": datetime.now().isoformat(),
        "name": name,
        "mode": mode,
        "level": level,
        "score": score,
        "lines": lines
    }
    scores.append(new_score)
    
    with open(SCORES_FILE, 'w', encoding='utf-8') as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)

def get_rankings(mode=None):
    """순위 가져오기"""
    scores = load_scores()
    if mode:
        scores = [s for s in scores if s.get('mode') == mode]
    
    # 점수 기준으로 정렬
    scores.sort(key=lambda x: x.get('score', 0), reverse=True)
    return scores[:10]  # 상위 10명만

# 세션 상태 초기화
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'final_score' not in st.session_state:
    st.session_state.final_score = 0
if 'final_level' not in st.session_state:
    st.session_state.final_level = 1
if 'final_lines' not in st.session_state:
    st.session_state.final_lines = 0

# 메인 타이틀
st.title("🎮 학생들과 함께하는 테트리스")

# 사이드바 - 게임 설정
with st.sidebar:
    st.header("⚙️ 게임 설정")
    
    # 게임 모드 선택
    game_mode = st.selectbox(
        "게임 모드",
        ["Easy", "Normal", "Hard"],
        help="Easy: 느린 속도 | Normal: 보통 속도 | Hard: 빠른 속도"
    )
    
    # 시작 레벨
    start_level = st.slider("시작 레벨", 1, 30, 1)
    
    st.divider()
    
    # 조작법 안내
    st.header("🎯 조작법")
    st.write("""
    - **←** : 왼쪽 이동
    - **→** : 오른쪽 이동  
    - **↓** : 빠르게 떨어뜨리기
    - **↑** : 블록 회전
    - **스페이스** : 한번에 떨어뜨리기
    """)

# 메인 영역
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🎲 게임 화면")
    
    # 게임 상태 표시
    if not st.session_state.game_over:
        status_col1, status_col2, status_col3 = st.columns(3)
        with status_col1:
            st.metric("모드", game_mode)
        with status_col2:
            st.metric("시작 레벨", start_level)
        with status_col3:
            st.metric("목표", f"{start_level * 10} 라인")
    
    # 테트리스 게임 HTML
    tetris_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 20px;
                background: #222;
                color: white;
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 80vh;
            }}
            .game-container {{
                display: flex;
                gap: 20px;
                align-items: flex-start;
            }}
            .game-board {{
                border: 3px solid #fff;
                background: #000;
            }}
            .info-panel {{
                background: #333;
                padding: 20px;
                border-radius: 10px;
                min-width: 200px;
            }}
            .next-piece {{
                width: 80px;
                height: 80px;
                border: 2px solid #666;
                background: #111;
                margin: 10px 0;
            }}
            .score {{
                font-size: 18px;
                margin: 10px 0;
            }}
            .game-over {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(0,0,0,0.9);
                padding: 30px;
                border-radius: 15px;
                text-align: center;
                border: 3px solid #ff4444;
            }}
            button {{
                background: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
                cursor: pointer;
                margin: 5px;
            }}
            button:hover {{
                background: #45a049;
            }}
            .restart-btn {{
                background: #ff4444;
            }}
            .restart-btn:hover {{
                background: #cc3333;
            }}
        </style>
    </head>
    <body>
        <div class="game-container">
            <canvas id="gameCanvas" class="game-board" width="300" height="600"></canvas>
            <div class="info-panel">
                <h3>게임 정보</h3>
                <div class="score">점수: <span id="score">0</span></div>
                <div class="score">레벨: <span id="level">{start_level}</span></div>
                <div class="score">라인: <span id="lines">0</span></div>
                <div class="score">모드: {game_mode}</div>
                
                <h4>다음 블록</h4>
                <canvas id="nextCanvas" class="next-piece" width="80" height="80"></canvas>
                
                <button onclick="startGame()">게임 시작</button>
                <button onclick="pauseGame()">일시정지</button>
                <button class="restart-btn" onclick="restartGame()">다시시작</button>
            </div>
        </div>
        
        <div id="gameOverModal" class="game-over" style="display: none;">
            <h2>🎯 게임 종료!</h2>
            <p>최종 점수: <span id="finalScore">0</span></p>
            <p>도달 레벨: <span id="finalLevel">1</span></p>
            <p>제거 라인: <span id="finalLines">0</span></p>
            <button onclick="saveScore()">점수 저장하기</button>
            <button class="restart-btn" onclick="restartGame()">다시 게임</button>
        </div>

        <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            const nextCanvas = document.getElementById('nextCanvas');
            const nextCtx = nextCanvas.getContext('2d');
            
            const BOARD_WIDTH = 10;
            const BOARD_HEIGHT = 20;
            const CELL_SIZE = 30;
            
            let board = Array(BOARD_HEIGHT).fill().map(() => Array(BOARD_WIDTH).fill(0));
            let currentPiece = null;
            let nextPiece = null;
            let score = 0;
            let level = {start_level};
            let lines = 0;
            let gameRunning = false;
            let gameLoop = null;
            
            // 게임 속도 설정
            const speeds = {{
                'Easy': 800,
                'Normal': 500,
                'Hard': 300
            }};
            let dropSpeed = speeds['{game_mode}'];
            
            // 테트리스 블록 정의
            const pieces = [
                // I
                [[[1,1,1,1]]],
                // O  
                [[[1,1],[1,1]]],
                // T
                [[[0,1,0],[1,1,1]], [[1,0],[1,1],[1,0]], [[1,1,1],[0,1,0]], [[0,1],[1,1],[0,1]]],
                // S
                [[[0,1,1],[1,1,0]], [[1,0],[1,1],[0,1]]],
                // Z
                [[[1,1,0],[0,1,1]], [[0,1],[1,1],[1,0]]],
                // J
                [[[1,0,0],[1,1,1]], [[1,1],[1,0],[1,0]], [[1,1,1],[0,0,1]], [[0,1],[0,1],[1,1]]],
                // L
                [[[0,0,1],[1,1,1]], [[1,0],[1,0],[1,1]], [[1,1,1],[1,0,0]], [[1,1],[0,1],[0,1]]]
            ];
            
            const colors = ['#00f', '#0f0', '#f00', '#ff0', '#f0f', '#0ff', '#ffa500'];
            
            function createPiece() {{
                const pieceIndex = Math.floor(Math.random() * pieces.length);
                return {{
                    shape: pieces[pieceIndex][0],
                    x: Math.floor(BOARD_WIDTH / 2) - 1,
                    y: 0,
                    color: colors[pieceIndex],
                    rotations: pieces[pieceIndex],
                    currentRotation: 0
                }};
            }}
            
            function drawCell(ctx, x, y, color) {{
                ctx.fillStyle = color;
                ctx.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
                ctx.strokeStyle = '#333';
                ctx.strokeRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
            }}
            
            function drawBoard() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                
                // 고정된 블록 그리기
                for (let y = 0; y < BOARD_HEIGHT; y++) {{
                    for (let x = 0; x < BOARD_WIDTH; x++) {{
                        if (board[y][x]) {{
                            drawCell(ctx, x, y, board[y][x]);
                        }}
                    }}
                }}
                
                // 현재 블록 그리기
                if (currentPiece) {{
                    for (let y = 0; y < currentPiece.shape.length; y++) {{
                        for (let x = 0; x < currentPiece.shape[y].length; x++) {{
                            if (currentPiece.shape[y][x]) {{
                                drawCell(ctx, currentPiece.x + x, currentPiece.y + y, currentPiece.color);
                            }}
                        }}
                    }}
                }}
            }}
            
            function drawNextPiece() {{
                nextCtx.clearRect(0, 0, nextCanvas.width, nextCanvas.height);
                if (nextPiece) {{
                    const cellSize = 15;
                    for (let y = 0; y < nextPiece.shape.length; y++) {{
                        for (let x = 0; x < nextPiece.shape[y].length; x++) {{
                            if (nextPiece.shape[y][x]) {{
                                nextCtx.fillStyle = nextPiece.color;
                                nextCtx.fillRect(x * cellSize + 10, y * cellSize + 10, cellSize, cellSize);
                            }}
                        }}
                    }}
                }}
            }}
            
            function canMove(piece, dx, dy, rotation = null) {{
                const shape = rotation !== null ? piece.rotations[rotation] : piece.shape;
                for (let y = 0; y < shape.length; y++) {{
                    for (let x = 0; x < shape[y].length; x++) {{
                        if (shape[y][x]) {{
                            const newX = piece.x + x + dx;
                            const newY = piece.y + y + dy;
                            
                            if (newX < 0 || newX >= BOARD_WIDTH || newY >= BOARD_HEIGHT) {{
                                return false;
                            }}
                            if (newY >= 0 && board[newY][newX]) {{
                                return false;
                            }}
                        }}
                    }}
                }}
                return true;
            }}
            
            function placePiece() {{
                for (let y = 0; y < currentPiece.shape.length; y++) {{
                    for (let x = 0; x < currentPiece.shape[y].length; x++) {{
                        if (currentPiece.shape[y][x]) {{
                            board[currentPiece.y + y][currentPiece.x + x] = currentPiece.color;
                        }}
                    }}
                }}
                
                // 라인 체크 및 제거
                clearLines();
                
                // 새 블록 생성
                currentPiece = nextPiece;
                nextPiece = createPiece();
                
                // 게임 오버 체크
                if (!canMove(currentPiece, 0, 0)) {{
                    gameOver();
                }}
            }}
            
            function clearLines() {{
                let linesCleared = 0;
                for (let y = BOARD_HEIGHT - 1; y >= 0; y--) {{
                    if (board[y].every(cell => cell !== 0)) {{
                        board.splice(y, 1);
                        board.unshift(Array(BOARD_WIDTH).fill(0));
                        linesCleared++;
                        y++; // 같은 줄 다시 체크
                    }}
                }}
                
                if (linesCleared > 0) {{
                    lines += linesCleared;
                    score += linesCleared * 100 * level;
                    level = Math.floor(lines / 10) + {start_level};
                    
                    // 레벨에 따른 속도 조정
                    dropSpeed = Math.max(speeds['{game_mode}'] - (level - {start_level}) * 50, 100);
                    
                    updateDisplay();
                }}
            }}
            
            function updateDisplay() {{
                document.getElementById('score').textContent = score;
                document.getElementById('level').textContent = level;
                document.getElementById('lines').textContent = lines;
            }}
            
            function gameLoop() {{
                if (!gameRunning) return;
                
                if (canMove(currentPiece, 0, 1)) {{
                    currentPiece.y++;
                }} else {{
                    placePiece();
                }}
                
                drawBoard();
                drawNextPiece();
                
                setTimeout(() => {{
                    if (gameRunning) {{
                        gameLoop();
                    }}
                }}, dropSpeed);
            }}
            
            function startGame() {{
                if (!gameRunning) {{
                    gameRunning = true;
                    if (!currentPiece) {{
                        currentPiece = createPiece();
                        nextPiece = createPiece();
                    }}
                    gameLoop();
                }}
            }}
            
            function pauseGame() {{
                gameRunning = !gameRunning;
                if (gameRunning) {{
                    gameLoop();
                }}
            }}
            
            function restartGame() {{
                board = Array(BOARD_HEIGHT).fill().map(() => Array(BOARD_WIDTH).fill(0));
                currentPiece = null;
                nextPiece = null;
                score = 0;
                level = {start_level};
                lines = 0;
                gameRunning = false;
                document.getElementById('gameOverModal').style.display = 'none';
                updateDisplay();
                drawBoard();
            }}
            
            function gameOver() {{
                gameRunning = false;
                document.getElementById('finalScore').textContent = score;
                document.getElementById('finalLevel').textContent = level;
                document.getElementById('finalLines').textContent = lines;
                document.getElementById('gameOverModal').style.display = 'block';
                
                // Streamlit에 게임 결과 전달
                window.parent.postMessage({{
                    type: 'gameOver',
                    score: score,
                    level: level,
                    lines: lines,
                    mode: '{game_mode}'
                }}, '*');
            }}
            
            function saveScore() {{
                window.parent.postMessage({{
                    type: 'saveScore',
                    score: score,
                    level: level,
                    lines: lines,
                    mode: '{game_mode}'
                }}, '*');
            }}
            
            // 키보드 이벤트
            document.addEventListener('keydown', (e) => {{
                if (!gameRunning || !currentPiece) return;
                
                switch(e.key) {{
                    case 'ArrowLeft':
                        e.preventDefault();
                        if (canMove(currentPiece, -1, 0)) {{
                            currentPiece.x--;
                            drawBoard();
                        }}
                        break;
                    case 'ArrowRight':
                        e.preventDefault();
                        if (canMove(currentPiece, 1, 0)) {{
                            currentPiece.x++;
                            drawBoard();
                        }}
                        break;
                    case 'ArrowDown':
                        e.preventDefault();
                        if (canMove(currentPiece, 0, 1)) {{
                            currentPiece.y++;
                            drawBoard();
                        }}
                        break;
                    case 'ArrowUp':
                        e.preventDefault();
                        const nextRotation = (currentPiece.currentRotation + 1) % currentPiece.rotations.length;
                        if (canMove(currentPiece, 0, 0, nextRotation)) {{
                            currentPiece.currentRotation = nextRotation;
                            currentPiece.shape = currentPiece.rotations[nextRotation];
                            drawBoard();
                        }}
                        break;
                    case ' ':
                        e.preventDefault();
                        while (canMove(currentPiece, 0, 1)) {{
                            currentPiece.y++;
                        }}
                        drawBoard();
                        break;
                }}
            }});
            
            // 초기 화면 그리기
            drawBoard();
            updateDisplay();
        </script>
    </body>
    </html>
    """
    
    # 게임 컴포넌트 렌더링
    game_component = components.html(tetris_html, height=700)

with col2:
    st.header("🏆 실시간 순위표")
    
    # 순위표 탭
    tab1, tab2, tab3, tab4 = st.tabs(["전체", "Easy", "Normal", "Hard"])
    
    with tab1:
        rankings = get_rankings()
        if rankings:
            for i, record in enumerate(rankings, 1):
                with st.container():
                    st.write(f"**{i}위** {record['name']}")
                    st.caption(f"점수: {record['score']:,} | 레벨: {record['level']} | 모드: {record['mode']}")
        else:
            st.info("아직 기록이 없습니다!")
    
    with tab2:
        rankings = get_rankings("Easy")
        if rankings:
            for i, record in enumerate(rankings, 1):
                st.write(f"**{i}위** {record['name']} - {record['score']:,}점")
        else:
            st.info("Easy 모드 기록이 없습니다!")
    
    with tab3:
        rankings = get_rankings("Normal")  
        if rankings:
            for i, record in enumerate(rankings, 1):
                st.write(f"**{i}위** {record['name']} - {record['score']:,}점")
        else:
            st.info("Normal 모드 기록이 없습니다!")
    
    with tab4:
        rankings = get_rankings("Hard")
        if rankings:
            for i, record in enumerate(rankings, 1):
                st.write(f"**{i}위** {record['name']} - {record['score']:,}점")
        else:
            st.info("Hard 모드 기록이 없습니다!")

# 점수 저장 처리
if st.session_state.game_over:
    st.success("🎯 게임이 종료되었습니다!")
    
    with st.form("score_form"):
        st.subheader("점수 기록하기")
        player_name = st.text_input("플레이어 이름", placeholder="이름을 입력하세요")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("최종 점수", f"{st.session_state.final_score:,}")
        with col2:
            st.metric("도달 레벨", st.session_state.final_level)
        with col3:
            st.metric("제거 라인", st.session_state.final_lines)
        
        if st.form_submit_button("점수 저장", use_container_width=True):
            if player_name.strip():
                save_score(
                    player_name.strip(),
                    game_mode,
                    st.session_state.final_level,
                    st.session_state.final_score,
                    st.session_state.final_lines
                )
                st.success(f"{player_name}님의 점수가 저장되었습니다!")
                st.session_state.game_over = False
                st.rerun()
            else:
                st.error("이름을 입력해주세요!")

# JavaScript 메시지 수신 처리
components.html("""
<script>
window.addEventListener('message', function(event) {
    if (event.data.type === 'gameOver') {
        // 게임 오버 정보를 Streamlit에 전달
        console.log('Game Over:', event.data);
    } else if (event.data.type === 'saveScore') {
        // 점수 저장 요청
        console.log('Save Score:', event.data);
    }
});
</script>
""", height=0)

# 푸터
st.divider()
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🎮 학생들과 함께하는 테트리스 게임 | Made with ❤️ using Streamlit</p>
    <p>키보드 조작: ←→ 이동, ↑ 회전, ↓ 빠른 낙하, 스페이스 즉시 낙하</p>
</div>
""", unsafe_allow_html=True)