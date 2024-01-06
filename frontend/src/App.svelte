<script>
  let attempt = 1;
  let letter = 0;

  let game = {
    attempts: [
      [
        { letter: "H", state: "grey" },
        { letter: "E", state: "yellow" },
        { letter: "L", state: "grey" },
        { letter: "L", state: "green" },
        { letter: "O", state: "grey" },
      ],
      [
        { letter: "", state: null },
        { letter: "", state: null },
        { letter: "", state: null },
        { letter: "", state: null },
        { letter: "", state: null },
      ],
      [
        { letter: "", state: null },
        { letter: "", state: null },
        { letter: "", state: null },
        { letter: "", state: null },
        { letter: "", state: null },
      ],
      [
        { letter: "", state: null },
        { letter: "", state: null },
        { letter: "", state: null },
        { letter: "", state: null },
        { letter: "", state: null },
      ],
      [
        { letter: "", state: null },
        { letter: "", state: null },
        { letter: "", state: null },
        { letter: "", state: null },
        { letter: "", state: null },
      ],
    ],
    letters: {
      grey: "",
      green: "l",
      yellow: "e",
    },
  };

  const keys = ["qwertyuiop", "asdfghjkl", "zxcvbnm"];

  const letter_background = (state) => {
    switch (state) {
      case "grey":
        return "bg-neutral-700";
      case "green":
        return "bg-green-400 bg-opacity-60";
      case "yellow":
        return "bg-amber-300 bg-opacity-60";
      case "unused":
        return "bg-neutral-400";
      default:
        return "border-neutral-700 border-2";
    }
  };

  const key_background = (key) => {
    if (game.letters.green.includes(key)) {
      return letter_background("green");
    } else if (game.letters.yellow.includes(key)) {
      return letter_background("yellow");
    } else if (game.letters.grey.includes(key)) {
      return letter_background("grey");
    } else {
      return letter_background("unused");
    }
  };

  const handleKeydown = (event) => {
    if (/^[a-zA-Z]$/.test(event.key) && letter < 5 && attempt < 6) {
      game.attempts[attempt][letter].letter = event.key;
      letter++;
    } else if (event.key == "Backspace" && letter > 0) {
      game.attempts[attempt][letter - 1].letter = "";
      letter--;
    } else if (event.key == "Enter" && letter == 5) {
      alert("send");
    }
  };
</script>

<svelte:window on:keydown={handleKeydown} />

<main class="flex flex-col items-center min-h-screen text-white bg-neutral-900">
  <h1 class="p-10 text-4xl font-bold">Lombardle</h1>
  <div class="grid grid-cols-5 grid-rows-6 gap-2 uppercase">
    {#each game.attempts as word}
      {#each word as letter}
        <span
          class={` text-3xl h-16 w-16 leading-[64px] text-center font-bold ${letter_background(
            letter.state
          )}`}>{letter.letter}</span
        >
      {/each}
    {/each}
  </div>
  <div class="flex flex-col items-center">
    {#each keys as row}
      <div class={` grid grid-cols-10`}>
        {#each row as letter}
          <span class={`text-xl font-bold p-4 ${key_background(letter)}`}
            >{letter}</span
          >
        {/each}
      </div>
    {/each}
  </div>
</main>
