import java.util.Scanner;

public class PlayerRoster {
   public static void main(String[] args) {
      Scanner scnr = new Scanner(System.in);
      final int NUM_PLAYERS = 5;
      int[] jerseyNums = new int[NUM_PLAYERS];
      int[] ratingNums = new int[NUM_PLAYERS];
      int i, j;
      int playerJersey;
      int playerRating;
      char menuOp;

      for (i = 0; i < NUM_PLAYERS; ++i) {
        System.out.println("Enter player " + (i + 1 + "'s jersey number:"));
        jerseyNums[i] = scnr.nextInt();

        System.out.println("Enter player " + (i + 1 + "'s rating:"));
        ratingNums[i] = scnr.nextInt();
        System.out.println("");
      }

      System.out.println("ROSTER");
      for (i = 0; i < NUM_PLAYERS; ++i) {
        System.out.println("Player " + (i + 1) + " -- Jersey number: " + jerseyNums[i] + ", Rating: " + ratingNums[i]);
      }


      //Menu 
      do {
        System.out.println("\nMENU");
        System.out.println("u - Update player rating");
        System.out.println("a - Output players above a rating");
        System.out.println("r - Replace player");
        System.out.println("o - Output roster");
        System.out.println("q - Quit");

        System.out.println("\nChoose an option:");
        menuOp = scnr.next().charAt(0);

        if (menuOp == 'u') {
            System.out.println("Enter a jersey number");
            playerJersey = scnr.nextInt();

            System.out.println("Enter a new rating for player");
            playerRating = scnr.nextInt();

            for (i = 0; i < NUM_PLAYERS; ++i) {
                if (jerseyNums[i] == playerJersey) {
                    ratingNums[i] = playerRating;
                }
            }
        }
        else if (menuOp == 'a') {
            System.out.println("Enter a rating:");
            playerRating = scnr.nextInt();

            System.out.println("\nABOVE " + playerRating);

            for (i = 0; i < NUM_PLAYERS; ++i) {
                if (ratingNums[i] > playerRating) {
                    System.out.println("Player " + (i + 1) + " -- Jersey number: " + jerseyNums[i] + ", Rating: " + ratingNums[i]);
                }
            }
        }
        else if (menuOp == 'r') {
            System.out.println("Enter a jersey number:");
            playerJersey = scnr.nextInt();
            j = -1;

            for (i = 0; i < NUM_PLAYERS; ++i) {
                if (playerJersey == jerseyNums[i]) {
                    j = i;
                }
            }

            if (j != -1) {
                System.out.println("Enter a new jersey number:");
                playerJersey = scnr.nextInt();

                System.out.println("Enter a rating for the new player");
                playerRating = scnr.nextInt();

                jerseyNums[j] = playerJersey;
                ratingNums[j] = playerRating;
            }
        }

        else if (menuOp == 'o') {
            System.out.println("ROSTER");
            for (i = 0; i < NUM_PLAYERS; ++i) {
                System.out.println("Player " + (i + 1) + " -- Jersey number: " + jerseyNums[i] + ", Rating: " + ratingNums[i]);
            }
        }
      } while (menuOp != 'q');
        

    }
}
