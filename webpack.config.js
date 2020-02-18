const path = require('path');
const ExtractTextPlugin = require("extract-text-webpack-plugin");

module.exports = {
  entry: '.blog/src/index.js',
  output: {
    path: path.resolve(__dirname, 'blog/static'),
    filename: 'js/bundle.js'
  },
  module: {
    rules: [{
      test: /\.scss$/,
      use: ExtractTextPlugin.extract({
        fallback: 'style-loader',
        use: [
          'css-loader',
          'sass-loader'
        ]
      })
    },
    {
      test: /\.(woff|woff2|eot|ttf|svg)$/,
      use: [{
        loader: 'file-loader',
        options: {
          name: '[name].[ext]',
          outputPath: 'fonts/'
        }
      }],
    }]
  },
  plugins: [
    new ExtractTextPlugin('styles.css'),
  ]
};
