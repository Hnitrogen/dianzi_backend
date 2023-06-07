#include <SFML/Graphics.hpp>
#include <random>
#include <cmath>

int main()
{
    constexpr int windowWidth = 800;
    constexpr int windowHeight = 600;
    constexpr float heartSize = 20.0f;
    constexpr float heartScale = 0.3f;
    constexpr float heartSpeed = 200.0f;
    constexpr float heartRadius = 100.0f;
    constexpr int numHearts = 100;

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<float> xDist(0, windowWidth);
    std::uniform_real_distribution<float> yDist(-heartRadius, -heartSize * heartScale);
    std::uniform_real_distribution<float> angleDist(0, 2 * M_PI);

    sf::RenderWindow window(sf::VideoMode(windowWidth, windowHeight), "Heart Rain");
    window.setFramerateLimit(60);

    sf::Texture heartTexture;
    heartTexture.loadFromFile("heart.png");
    heartTexture.setSmooth(true);

    std::vector<sf::Sprite> hearts;
    hearts.reserve(numHearts);

    for (int i = 0; i < numHearts; i++) {
        float x = xDist(gen);
        float y = yDist(gen);
        float angle = angleDist(gen);
        sf::Sprite heart(heartTexture);
        heart.setScale(heartScale, heartScale);
        heart.setPosition(x, y);
        heart.setRotation(angle * 180 / M_PI);
        hearts.push_back(heart);
    }

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) {
                window.close();
            }
        }

        window.clear();

        for (auto& heart : hearts) {
            float x = heart.getPosition().x;
            float y = heart.getPosition().y;
            float angle = heart.getRotation() * M_PI / 180;
            x += heartSpeed * std::cos(angle) * window.getFrameTime().asSeconds();
            y += heartSpeed * std::sin(angle) * window.getFrameTime().asSeconds();
            if (y > windowHeight + heartSize * heartScale) {
                y = yDist(gen);
                x = xDist(gen);
                angle = angleDist(gen);
                heart.setRotation(angle * 180 / M_PI);
            }
            heart.setPosition(x, y);
            window.draw(heart);
        }

        window.display();
    }

    return 0;
}
